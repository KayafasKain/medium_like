from django.db import models
from django.apps import apps
from django.db.models.signals import post_save
from django.contrib.auth import (
    get_user_model
)

import channels.layers
channel_layer = channels.layers.get_channel_layer()
from asgiref.sync import async_to_sync

User = get_user_model()

class PostArticle(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=128)
    text = models.CharField(max_length=1024)
    category = models.ForeignKey('Category', null=True, on_delete=models.SET_NULL)
    status = models.ForeignKey('Status', null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

def create_post(sender, **kwargs):
    if kwargs['created']:
        async_to_sync(channel_layer.group_send)('main_channel', {'type':'new_post', 'message': PostArticle.objects.last().pk})

post_save.connect(create_post)

class Status(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return '{}'.format(self.name)

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return '{}'.format(self.name)