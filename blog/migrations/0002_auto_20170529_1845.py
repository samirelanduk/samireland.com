# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='body',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='blogpost',
            name='date',
            field=models.DateField(default=datetime.date(2017, 5, 29)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='blogpost',
            name='title',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='blogpost',
            name='visible',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
