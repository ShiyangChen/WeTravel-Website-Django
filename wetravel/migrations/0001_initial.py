# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('login_user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
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
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=15)),
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
                ('address', models.CharField(max_length=200)),
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
                ('place_type', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('is_visible', models.BooleanField(default=False)),
                ('link', models.URLField(max_length=500)),
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
                ('status', models.BooleanField(default=False)),
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
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('avatar', models.ImageField(upload_to=b'images/', null=True, verbose_name=b'Profile Pic', blank=True)),
                ('friends', models.ManyToManyField(related_name='friends_rel_+', to='wetravel.UserProfile')),
                ('region', models.ForeignKey(to='wetravel.Region', null=True)),
                ('requests', models.ManyToManyField(related_name='requests_rel_+', to='wetravel.UserProfile')),
                ('to_visit', models.ForeignKey(related_name='places_to_visit', to='wetravel.Place', null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
                ('visited', models.ManyToManyField(related_name='places_visited', null=True, to='wetravel.Place')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='travel',
            name='members',
            field=models.ManyToManyField(to='wetravel.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='request',
            name='sent_for',
            field=models.ManyToManyField(related_name='sent_for', to='wetravel.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='request',
            name='sent_from',
            field=models.ManyToManyField(related_name='sent_from', to='wetravel.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='request',
            name='sent_to',
            field=models.ManyToManyField(related_name='sent_to', to='wetravel.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='publisher',
            field=models.ForeignKey(related_name='publisher', to='wetravel.UserProfile', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='restricted_members',
            field=models.ManyToManyField(related_name='restricted_members', to='wetravel.UserProfile'),
            preserve_default=True,
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
            model_name='group',
            name='members',
            field=models.ManyToManyField(to='wetravel.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='place',
            field=models.ForeignKey(to='wetravel.Place', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='to_post',
            field=models.ForeignKey(to='wetravel.Post', null=True),
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
    ]
