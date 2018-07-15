from rest_framework import serializers
from .models import (Status, Category, PostArticle)


class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Status
        fields = (
            'id',
            'name',
        )

class CategotySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            'id',
            'name',
        )

class PostSerializer(serializers.ModelSerializer):
    # category = CategotySerializer(read_only=False)
    # status = StatusSerializer(read_only=False)

    class Meta:
        model = PostArticle
        fields = (
            'id',
            'title',
            'description',
            'text',
            'category',
            'status',
            'user'
        )