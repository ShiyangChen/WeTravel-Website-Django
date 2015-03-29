from django.db import models

# Create your models here.

class User(models.Model):
    email      = models.EmailField(max_length=30)
    first_name = models.CharField(max_length=20)
    last_name  = models.CharField(max_length=20)
    password   = models.CharField(max_length=15)

class Post(models.Model):
    text      = models.TextField()
    publisher = models.ForeignKey(User)
    link      = models.URLField(max_length=500)

class Group(models.Model):
    name   = models.CharField(max_length=15)
    member = models.ManyToManyField(User)
