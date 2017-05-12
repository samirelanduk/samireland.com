# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import media.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MediaFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('mediatitle', models.TextField(unique=True, default='')),
                ('mediafile', models.FileField(upload_to=media.models.create_filename)),
            ],
        ),
    ]
