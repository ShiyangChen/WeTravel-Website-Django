# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wetravel', '0002_auto_20150430_0531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='to_visit',
            field=models.ForeignKey(related_name='places_to_visit', to='wetravel.Place', null=True),
            preserve_default=True,
        ),
    ]
