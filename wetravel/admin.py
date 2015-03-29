from django.contrib import admin
from wetravel.models import User, Group

# Register your models here.

admin.site.register([User, Group])
