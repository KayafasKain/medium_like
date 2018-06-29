from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import (
    get_user_model
)

User = get_user_model()
class Profile(models.Model):
    phone_number = PhoneNumberField(blank=True, null=True)
    about = models.CharField(blank=True, null=True, max_length=256)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

