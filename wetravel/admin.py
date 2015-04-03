from django.contrib import admin
from wetravel.models import UserProfile, Group

# Register your models here.

admin.site.register([UserProfile, Group])
