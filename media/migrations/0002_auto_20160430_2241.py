# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='imagetitle',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='image',
            name='imagefile',
            field=models.FileField(upload_to='images'),
        ),
    ]
