# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wetravel', '0004_auto_20150501_1544'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Accommodation',
            new_name='Accomodation',
        ),
    ]
