# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('wetravel', '0002_auto_20150501_1152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='login_user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
