# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import media.models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0004_auto_20160501_1405'),
    ]

    operations = [
        migrations.CreateModel(
            name='MediaFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('mediaitle', models.TextField(unique=True, default='')),
                ('mediafile', models.FileField(upload_to=media.models.create_filename)),
            ],
        ),
        migrations.DeleteModel(
            name='Image',
        ),
    ]
