# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wetravel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accommodation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('check_in_time', models.DateTimeField()),
                ('check_out_time', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField()),
                ('note', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(max_length=200)),
                ('function', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('country', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField()),
                ('status', models.CharField(max_length=10)),
                ('sent_for', models.ManyToManyField(related_name=b'sent_for', to='wetravel.User')),
                ('sent_from', models.ManyToManyField(related_name=b'sent_from', to='wetravel.User')),
                ('sent_to', models.ManyToManyField(related_name=b'sent_to', to='wetravel.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Travel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('destination', models.ForeignKey(to='wetravel.Region', null=True)),
                ('members', models.ManyToManyField(to='wetravel.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='place',
            name='region',
            field=models.ForeignKey(to='wetravel.Region', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hotel',
            name='region',
            field=models.ForeignKey(to='wetravel.Region', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='place',
            field=models.ForeignKey(to='wetravel.Place', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='accommodation',
            name='hotel',
            field=models.ForeignKey(to='wetravel.Hotel', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='accommodation',
            name='travel',
            field=models.ForeignKey(to='wetravel.Travel', null=True),
            preserve_default=True,
        ),
        migrations.RenameField(
            model_name='group',
            old_name='member',
            new_name='members',
        ),
        migrations.AddField(
            model_name='post',
            name='invisible_to',
            field=models.ManyToManyField(related_name=b'invisivle_to', to='wetravel.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='friends',
            field=models.ManyToManyField(related_name='friends_rel_+', to='wetravel.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='region',
            field=models.ForeignKey(to='wetravel.Region', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='to_visit',
            field=models.ManyToManyField(related_name=b'places_to_visit', to='wetravel.Place'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='visited',
            field=models.ManyToManyField(related_name=b'places_visited', to='wetravel.Place'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='publisher',
            field=models.ForeignKey(related_name=b'publisher', to='wetravel.User', null=True),
        ),
    ]
