# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wetravel', '0003_auto_20150425_2059'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='travel',
            field=models.ForeignKey(to='wetravel.Travel', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='travel',
            name='desc',
            field=models.CharField(max_length=500, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='travel',
            name='groups',
            field=models.ManyToManyField(to='wetravel.Group'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='travel',
            name='name',
            field=models.CharField(max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(upload_to=b'images/', null=True, verbose_name=b'Profile Pic', blank=True),
            preserve_default=True,
        ),
    ]
