from django.contrib import admin

from django.apps import apps

Status = apps.get_model('post_app', 'Status')
Category = apps.get_model('post_app', 'Category')
PostArticle = apps.get_model('post_app', 'PostArticle')

admin.site.register(Status)
admin.site.register(Category)
admin.site.register(PostArticle)