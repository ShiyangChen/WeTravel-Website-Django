from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Region(models.Model):
    country = models.CharField(max_length=50)
    state   = models.CharField(max_length=50)
    city    = models.CharField(max_length=50)

    def __unicode__(self):
        return self.country + '/' + self.state + '/' + self.city

class Place(models.Model):
    address  = models.CharField(max_length=200)
    type = models.CharField(max_length=30)
    region   = models.ForeignKey(Region, null=True)

class UserProfile(models.Model):
    user     = models.OneToOneField(User)
    region   = models.ForeignKey(Region, null=True)
    friends  = models.ManyToManyField('self')
    to_visit = models.ManyToManyField(Place, related_name='places_to_visit')
    visited  = models.ManyToManyField(Place, related_name='places_visited')

    def __unicode__(self):
        return self.user.username

class Post(models.Model):
    text         = models.TextField()
    publisher    = models.ForeignKey(UserProfile, related_name='publisher', null=True)
    restricted_members = models.ManyToManyField(UserProfile, related_name='restricted_members')
    is_visible = models.BooleanField(default=False)
    link         = models.URLField(max_length=500)

class Group(models.Model):
    name    = models.CharField(max_length=15)
    members = models.ManyToManyField(UserProfile)

class Travel(models.Model):
    start_time  = models.DateTimeField()
    end_time    = models.DateTimeField()
    destination = models.ForeignKey(Region, null=True)
    members     = models.ManyToManyField(UserProfile)

class Hotel(models.Model):
    name    = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    phone   = models.CharField(max_length=30)
    region  = models.ForeignKey(Region, null=True)

class Event(models.Model):
    time  = models.DateTimeField()
    note  = models.TextField()
    place = models.ForeignKey(Place, null=True)

class Accommodation(models.Model):
    check_in_time  = models.DateTimeField()
    check_out_time = models.DateTimeField()
    hotel          = models.ForeignKey(Hotel, null=True)
    travel         = models.ForeignKey(Travel, null=True)

class Request(models.Model):
    time      = models.DateTimeField()
    status    = models.BooleanField(default=False)
    sent_from = models.ManyToManyField(UserProfile, related_name='sent_from')
    sent_to   = models.ManyToManyField(UserProfile, related_name='sent_to')
    sent_for  = models.ManyToManyField(UserProfile, related_name='sent_for')
