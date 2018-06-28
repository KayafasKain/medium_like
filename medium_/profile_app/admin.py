from django.contrib import admin

# Register your models here.
from django.apps import apps

Profile = apps.get_model('profile_app', 'Profile')
Contact = apps.get_model('profile_app', 'Contact')
EmploymentType = apps.get_model('profile_app', 'EmploymentType')
ClientClass = apps.get_model('profile_app', 'ClientClass')

admin.site.register(Profile)
admin.site.register(Contact)
admin.site.register(EmploymentType)
admin.site.register(ClientClass)
