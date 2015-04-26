# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wetravel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(upload_to=b'images/', null=True, verbose_name=b'Profile Pic', blank=True),
            preserve_default=True,
        ),
    ]
