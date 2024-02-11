import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
import django; django.setup()

import sys
import json
import subprocess
from django.core.management import call_command
from wagtail.models import Site
from core.models import HomePage

hostname = "samireland.com" if len(sys.argv) == 1 else sys.argv[1]
container_name = "sidc_django"

# Get dump from live site
subprocess.call(f'ssh {hostname} "docker exec {container_name} python manage.py dumpdata > dump.json"', shell=True, stderr=subprocess.DEVNULL)
subprocess.call(f'scp {hostname}:dump.json ./', shell=True, stderr=subprocess.DEVNULL)
subprocess.call(f'ssh {hostname} "rm dump.json"', shell=True, stderr=subprocess.DEVNULL)

# Make new DB
subprocess.call("rm db.sqlite3", shell=True, stderr=subprocess.DEVNULL)
subprocess.call("rm -rf ../media", shell=True, stderr=subprocess.DEVNULL)
subprocess.call("mkdir ../media", shell=True, stderr=subprocess.DEVNULL)
call_command("migrate", interactive=False, verbosity=0)

# Dump to get content types
call_command("dumpdata", indent=2, output="ct.json")
with open("ct.json") as f:
    content_types = [{
        "id": f["pk"],
        "model": f"{f['fields']['app_label']}.{f['fields']['model']}"
    } for f in json.load(f) if f["model"] == "contenttypes.contenttype"]

# Make copy of dump with updated content types
with open("dump.json") as f:
    data = json.load(f)
ct_lookup = {}
for f in data:
    if f["model"] == "contenttypes.contenttype":
        matching_ct = [c for c in content_types if
            f"{f['fields']['app_label']}.{f['fields']['model']}" == c["model"]
        ][0]
        ct_lookup[f["pk"]] = matching_ct["id"]
        f["pk"] = matching_ct["id"]
for f in data:
    if "content_type" in f["fields"]:
        f["fields"]["content_type"] = ct_lookup[f["fields"]["content_type"]]
with open("updated_dump.json", "w") as f:
    json.dump(data, f, indent=2)

# Update site
site = Site.objects.first()
site.hostname = hostname
site.site_name = hostname
site.save()

# Make dump2
with open("updated_dump.json") as f:
    data = json.load(f)
homepage_fixtures = [f for f in data if f["model"] == "core.homepage"
    or f["model"] == "wagtailcore.page" or f["model"] == "wagtailcore.revision"
    or f["model"] == "auth.user"]
with open("dump2.json", "w") as f:
    json.dump(homepage_fixtures, f, indent=2)

# Load home page
call_command("loaddata", "dump2.json")

# Set as default site
old_home_page = site.root_page
home_page = HomePage.objects.first()
site.root_page = home_page
site.save()
old_home_page.delete()

# Make dump3
other_fixtures = [f for f in data if f["model"].split(".")[0] in [
    "core", "articles", "projects", "about", "taggeditem", "wagtailimages"
]]
with open("dump3.json", "w") as f:
    json.dump(other_fixtures, f, indent=2)

# Load rest
call_command("loaddata", "dump3.json")

# Remove dumps
for f in ["dump.json", "ct.json", "updated_dump.json", "dump2.json", "dump3.json"]:
    os.remove(f)

# Get media
subprocess.call(f'ssh {hostname} "docker cp {container_name}:/home/app/media ./"', shell=True, stderr=subprocess.DEVNULL)
subprocess.call('rm -r ../media', shell=True, stderr=subprocess.DEVNULL)
subprocess.call(f'scp -r {hostname}:media ../', shell=True, stderr=subprocess.DEVNULL)
subprocess.call(f'ssh {hostname} "rm -r media"', shell=True, stderr=subprocess.DEVNULL)