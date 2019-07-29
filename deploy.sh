host="samireland.com"

# Empty the current source directory on the server
ssh sam@$host "rm -r ~/$host/source/* >& /dev/null"

# Send git tracked files
rsync -vr . --exclude-from='.gitignore' --exclude='.git' sam@$host:~/$host/source

# Copy secrets
scp core/secrets.py sam@$host:~/$host/source/core/secrets.py

# Turn off debug on server
ssh sam@$host "sed -i s/\"DEBUG = True\"/\"DEBUG = False\"/g ~/$host/source/core/settings.py"

# Add allowed host
ssh sam@$host "sed -i s/\"HOSTS = \[\]\"/\"HOSTS = \['$host', 'www.$host'\]\"/g ~/$host/source/core/settings.py"

# Install pip packages
ssh sam@$host "~/$host/env/bin/pip install -r ~/$host/source/requirements.txt"

# Switch database
ssh sam@$host "sed -i s/\"DATABASES = local\"/\"DATABASES = live\"/g ~/$host/source/core/secrets.py"

# Migrate
ssh sam@$host "cd ~/$host/source && ../env/bin/python manage.py migrate"

# Move static files
ssh sam@$host "cd ~/$host/source && ../env/bin/python manage.py compilescss"
ssh sam@$host "cd ~/$host/source && ../env/bin/python manage.py collectstatic --noinput"
