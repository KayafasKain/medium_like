from django.contrib import admin

# Register your models here.
from django.apps import apps

Profile = apps.get_model('profile_app', 'Profile')


admin.site.register(Profile)

