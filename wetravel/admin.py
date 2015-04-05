from django.contrib import admin
from wetravel.models import *

# Register your models here.

admin.site.register([UserProfile, Group])
