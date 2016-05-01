# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import media.models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0003_auto_20160430_2325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='imagefile',
            field=models.FileField(upload_to=media.models.create_filename),
        ),
    ]
