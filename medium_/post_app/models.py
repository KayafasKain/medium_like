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
    review = models.BooleanField(default=False)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
