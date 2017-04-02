import subprocess
import os
import sys

# What is the site name?
if len(sys.argv) < 2:
    print("What is the site name?")
    sys.exit()
sitename = sys.argv[1]

# Remove contents of remote source directory
subprocess.call(
 "ssh %s 'rm -r ~/%s/source/*'" % (sitename, sitename), shell=True
)

# What branch are we on?
branch = subprocess.check_output("git branch", shell=True).decode()
branches = branch.split("\n")
current_branch = [branch for branch in branches if branch.startswith("*")][0]
branch = current_branch.split()[1]

# What files is git tracking?
tracked_files = subprocess.check_output(
 "git ls-tree %s --name-only" % branch, shell=True
).decode()
tracked_files = filter(bool, tracked_files.split("\n"))

# Push source code to remote
for tracked_file in tracked_files:
    subprocess.call(
     "scp -r ./%s %s:~/%s/source/" % (tracked_file, sitename, sitename), shell=True
    )

# Turn off Debug
subprocess.call(
 "ssh %s 'sed -i s/\"DEBUG = True\"/\"DEBUG = False\"/g ~/%s/source/samireland/settings.py'" % (sitename, sitename),
 shell=True
)

# Add allowed hosts
subprocess.call(
 "ssh %s 'sed -i s/\"ALLOWED_HOSTS = \[\]\"/\"ALLOWED_HOSTS = \[£'%s£', £'www.%s£'\]\"/g ~/%s/source/samireland/settings.py'" % (sitename, sitename, sitename, sitename),
 shell=True
)
subprocess.call(
 "ssh %s 'sed -i s/£/\\\"/g ~/%s/source/samireland/settings.py'" % (sitename, sitename),
 shell=True
)

# Add google analytics
if sitename == "samireland.com":
    subprocess.call(
     "ssh %s 'sed -i s/\"<!--analytics-->\"/\"\{%% include \\\"analytics.html\\\" %%\}\"/g ~/%s/source/samireland/templates/base.html'" % (sitename, sitename),
     shell=True
    )

# Upload the secret settings
subprocess.call(
 "scp -r ./samireland/secrets.py %s:~/%s/source/samireland/secrets.py" % (sitename, sitename), shell=True
)

# Switch to postgres database remotely
subprocess.call(
 "ssh %s 'sed -i s/\": local_db\"/\": live_db\"/g ~/%s/source/samireland/secrets.py'" % (sitename, sitename),
 shell=True
)

# Install pip packages
subprocess.call(
 "ssh %s '~/%s/env/bin/pip install -r ~/%s/source/requirements.txt'" % (sitename, sitename, sitename),
 shell=True
)

# Apply migrations
subprocess.call(
 "ssh %s '~/%s/env/bin/python ~/%s/source/manage.py migrate'" % (sitename, sitename, sitename),
 shell=True
)

# Deploy static files
subprocess.call(
 "ssh %s 'cd ~/%s/source && ../env/bin/python manage.py collectstatic --noinput'" % (sitename, sitename),
 shell=True
)
