#!/usr/bin/env bash

ssh samireland.com 'cd samireland.com/source;source ../env/bin/activate;\
python manage.py dumpdata --exclude=contenttypes --exclude=auth.Permission\
> dump.json'

scp samireland.com:~/samireland.com/source/dump.json ./dump.json

if [[ "$1" = "files" ]] ; then
    rm ./uploads/*
    scp samireland.com:~/samireland.uk/uploads/* ./uploads/
fi

ssh samireland.com 'rm samireland.com/source/dump.json'

rm db.sqlite3

python manage.py migrate

python manage.py loaddata dump.json

rm dump.json

echo "from django.contrib.auth.models import User; User.objects.create_superuser('sam', 'admin@example.com', 'password')" | python manage.py shell
