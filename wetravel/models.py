from django.db import models

# Create your models here.

class Region(models.Model):
    country = models.CharField(max_length=50)
    state   = models.CharField(max_length=50)
    city    = models.CharField(max_length=50)

class Place(models.Model):
    address  = models.CharField(max_length=200)
    function = models.CharField(max_length=30)
    region   = models.ForeignKey(Region, null=True)

class User(models.Model):
    email      = models.EmailField(max_length=30)
    first_name = models.CharField(max_length=20)
    last_name  = models.CharField(max_length=20)
    password   = models.CharField(max_length=15) # password field?
    region     = models.ForeignKey(Region, null=True)
    friends    = models.ManyToManyField('self')
    to_visit   = models.ManyToManyField(Place, related_name='places_to_visit')
    visited    = models.ManyToManyField(Place, related_name='places_visited')

class Post(models.Model):
    text         = models.TextField()
    publisher    = models.ForeignKey(User, related_name='publisher', null=True)
    invisible_to = models.ManyToManyField(User, related_name='invisivle_to')
    link         = models.URLField(max_length=500)

class Group(models.Model):
    name    = models.CharField(max_length=15)
    members = models.ManyToManyField(User)

class Travel(models.Model):
    start_time  = models.DateTimeField()
    end_time    = models.DateTimeField()
    destination = models.ForeignKey(Region, null=True)
    members     = models.ManyToManyField(User)

class Hotel(models.Model):
    name    = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    phone   = models.CharField(max_length=30) # ?
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
    status    = models.CharField(max_length=10) # ?
    sent_from = models.ManyToManyField(User, related_name='sent_from')
    sent_to   = models.ManyToManyField(User, related_name='sent_to')
    sent_for  = models.ManyToManyField(User, related_name='sent_for')
