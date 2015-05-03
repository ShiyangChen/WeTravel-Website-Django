# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wetravel', '0005_auto_20150501_1716'),
    ]

    operations = [
        migrations.AddField(
            model_name='travel',
            name='end_date',
            field=models.DateField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='travel',
            name='start_date',
            field=models.DateField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='travel',
            name='end_time',
            field=models.TimeField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='travel',
            name='start_time',
            field=models.TimeField(null=True),
            preserve_default=True,
        ),
    ]
