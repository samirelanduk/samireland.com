# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0002_auto_20160430_2241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='imagetitle',
            field=models.TextField(unique=True, default=''),
        ),
    ]
