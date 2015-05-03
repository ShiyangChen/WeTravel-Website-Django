from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver 
from django.conf import settings

# Create your models here.

class Region(models.Model):
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)

    def __unicode__(self):
        return self.city  + ',' + self.state + ',' + self.country


class Place(models.Model):
    address  = models.CharField(max_length=200)
    place_type = models.CharField(max_length=30)
    region   = models.ForeignKey(Region, null=True)

    def __unicode__(self):
        return self.address + ',' + unicode(self.region)

class PlaceComment(models.Model):
    place = models.ForeignKey(Place, null=True)
    text = models.CharField(max_length=500)

    def __unicode__(self):
        return self.text

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    region = models.ForeignKey(Region, null=True)
    friends = models.ManyToManyField('self', related_name='friends')
    to_visit = models.ForeignKey(Place, related_name='places_to_visit', null=True)
    visited = models.ManyToManyField(Place, related_name='places_visited', null=True)
    requests = models.ManyToManyField('self', related_name='requests1', symmetrical=False)
    avatar = models.ImageField("Profile Pic", upload_to="images/", blank=True, null=True)

    def avatar_image(self):
        if self.avatar:
            return (settings.MEDIA_URL + self.avatar.name) 
        else:
            return "/static/images/default_image.png"

    def __unicode__(self):
        return self.user.username

class Post(models.Model):
    text = models.TextField()
    publisher = models.ForeignKey(UserProfile, related_name='publisher', null=True)
    restricted_members = models.ManyToManyField(UserProfile, related_name='restricted_members')
    is_visible = models.BooleanField(default=False)
    link = models.URLField(max_length=500)
    def __unicode__(self):
        return self.text

class Group(models.Model):
    name = models.CharField(max_length=15)
    members = models.ManyToManyField(UserProfile)

class Travel(models.Model):
    name = models.CharField(max_length=200,null=True)
    desc = models.CharField(max_length=500,null=True)
    start_date=models.DateField(null=True)
    end_date=models.DateField(null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    destination = models.ForeignKey(Region, null=True)
    members = models.ManyToManyField(UserProfile)
    groups=models.ManyToManyField(Group)

class Hotel(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=30)
    region = models.ForeignKey(Region, null=True)

class Event(models.Model):
    time = models.DateTimeField()
    note = models.TextField()
    place = models.ForeignKey(Place, null=True)
    travel = models.ForeignKey(Travel, null=True)

class Accomodation(models.Model):
    check_in_time = models.DateTimeField()
    check_out_time = models.DateTimeField()
    hotel = models.ForeignKey(Hotel, null=True)
    travel = models.ForeignKey(Travel, null=True)

class Request(models.Model):
    time = models.DateTimeField()
    status = models.BooleanField(default=False)
    sent_from = models.ManyToManyField(UserProfile, related_name='sent_from')
    sent_to = models.ManyToManyField(UserProfile, related_name='sent_to')
    sent_for = models.ManyToManyField(UserProfile, related_name='sent_for')


class Comment(models.Model):
    login_user = models.ForeignKey(User)
    text=models.TextField()
    to_post=models.ForeignKey(Post, null=True)
