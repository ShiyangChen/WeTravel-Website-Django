# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wetravel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='to_visit',
            field=models.ForeignKey(related_name='places_to_visit', to='wetravel.Place'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='visited',
            field=models.ManyToManyField(related_name='places_visited', null=True, to='wetravel.Place'),
            preserve_default=True,
        ),
    ]
