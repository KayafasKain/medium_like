from django.db import models
from django.apps import apps
from django.contrib.auth import (
    get_user_model
)

User = get_user_model()
class PostArticle(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=128)
    text = models.CharField(max_length=1024)
    category = models.ForeignKey('Category', null=True, on_delete=models.SET_NULL)
    status = models.ForeignKey('Status', null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

class Status(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return '{}'.format(self.name)

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return '{}'.format(self.name)