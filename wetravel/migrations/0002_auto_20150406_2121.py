# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wetravel', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='place',
            old_name='function',
            new_name='place_type',
        ),
        migrations.RemoveField(
            model_name='post',
            name='invisible_to',
        ),
        migrations.AddField(
            model_name='post',
            name='is_visible',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='restricted_members',
            field=models.ManyToManyField(related_name='restricted_members', to='wetravel.UserProfile'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hotel',
            name='address',
            field=models.CharField(max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='request',
            name='status',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
