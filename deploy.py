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
 "ssh {} 'rm -r ~/{}/source/* >& /dev/null'".format(sitename, sitename), shell=True
)

# What files are being tracked by git?
tracked_files = subprocess.check_output("git ls-files", shell=True).decode()
tracked_files = list(filter(bool, tracked_files.split("\n")))

# Push source code to remote
for file_ in tracked_files:
    directory = "/".join(file_.split("/")[:-1])
    subprocess.call(
     "ssh {} 'mkdir -p ~/{}/source/{}'".format(sitename, sitename, directory), shell=True
    )
    subprocess.call(
     "scp -r ./{} {}:~/{}/source/{}".format(file_, sitename, sitename, file_), shell=True
    )

# Turn off Debug
subprocess.call(
 "ssh {} 'sed -i s/\"DEBUG = True\"/\"DEBUG = False\"/g ~/{}/source/samireland/settings.py'".format(sitename, sitename),
 shell=True
)

# Add allowed hosts
subprocess.call(
 "ssh {} 'sed -i s/\"ALLOWED_HOSTS = \[\]\"/\"ALLOWED_HOSTS = \[£'{}£', £'www.{}£'\]\"/g ~/{}/source/samireland/settings.py'".format(sitename, sitename, sitename, sitename),
 shell=True
)
subprocess.call(
 "ssh {} 'sed -i s/£/\\\"/g ~/{}/source/samireland/settings.py'".format(sitename, sitename),
 shell=True
)

# Change where uploaded files are stored
if sitename == "samireland.uk":
    subprocess.call(
     "ssh {} 'sed -i s/\"BASE_DIR, \\\"uploads\\\"\"/\"\\\"..\\\", \\\"uploads\\\"\"/g ~/{}/source/samireland/settings.py'".format(sitename, sitename),
     shell=True
    )
else:
    subprocess.call(
     "ssh {} 'sed -i s/\"BASE_DIR, \\\"uploads\\\"\"/\"\\\"..\\\", \\\"..\\\", \\\"samireland.uk\\\", \\\"uploads\\\"\"/g ~/{}/source/samireland/settings.py'".format(sitename, sitename),
     shell=True
    )

# Add google analytics
if sitename == "samireland.com":
    subprocess.call(
     "ssh {} 'sed -i s/\"<!--analytics-->\"/\"\{{% include \\\"analytics.html\\\" %\}}\"/g ~/{}/source/samireland/templates/base.html'".format(sitename, sitename),
     shell=True
    )

# Upload the secret settings
subprocess.call(
 "scp -r ./samireland/secrets.py {}:~/{}/source/samireland/secrets.py".format(sitename, sitename), shell=True
)

# Switch to postgres database remotely
subprocess.call(
 "ssh {} 'sed -i s/\"= local\"/\"= live\"/g ~/{}/source/samireland/secrets.py'".format(sitename, sitename),
 shell=True
)

# Install pip packages
subprocess.call(
 "ssh {} '~/{}/env/bin/pip install -r ~/{}/source/requirements.txt'".format(sitename, sitename, sitename),
 shell=True
)

# Apply migrations
subprocess.call(
 "ssh {} '~/{}/env/bin/python ~/{}/source/manage.py migrate'".format(sitename, sitename, sitename),
 shell=True
)

# Deploy static files
subprocess.call(
 "ssh {} 'cd ~/{}/source && ../env/bin/python manage.py compilescss'".format(sitename, sitename),
 shell=True
)
subprocess.call(
 "ssh {} 'cd ~/{}/source && ../env/bin/python manage.py collectstatic --noinput'".format(sitename, sitename),
 shell=True
)
