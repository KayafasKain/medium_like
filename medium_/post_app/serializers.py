from rest_framework import serializers
from django.apps import apps

PostArticle = apps.get_model('post_app', 'PostArticle')
Status = apps.get_model('post_app', 'Status')
Categoty = apps.get_model('post_app', 'Category')

class PostSerializer(serializers.ModelSerializer):
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

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = (
            'id',
            'name',
        )

class CategotySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoty
        fields = (
            'id',
            'name',
        )
