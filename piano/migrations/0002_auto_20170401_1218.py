# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('piano', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='practicesession',
            name='date',
            field=models.DateField(unique=True),
        ),
    ]
