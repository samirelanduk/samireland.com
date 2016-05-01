# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0005_auto_20160501_2044'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mediafile',
            old_name='mediaitle',
            new_name='mediatitle',
        ),
    ]
