from django.apps import apps
from django.contrib.auth import (
    get_user_model,
)

from .serializers import PostSerializer, StatusSerializer, CategotySerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

PostArticle = apps.get_model('post_app', 'PostArticle')
Status = apps.get_model('post_app', 'Status')
Categoty = apps.get_model('post_app', 'Category')

class PostArticleView(APIView):
    context_object_name = 'api-post'

    def get(self, request, format=None):
        posts = PostArticle.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        post = PostArticle.objects.get(pk=pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        post = PostArticle.objects.get(pk=pk)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        post = PostArticle.objects.get(pk=pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

post_view = PostArticleView.as_view()

class StatusView(APIView):
    context_object_name = 'api-status'

    def get(self, request, format=None):
        status = Status.objects.all()
        serializer = StatusSerializer(status, many=True)
        return Response(serializer.data)

status_view = StatusView.as_view()

class CategoryView(APIView):
    context_object_name = 'api-category'

    def get(self, request, format=None):
        categories = Categoty.objects.all()
        serializer = CategotySerializer(categories, many=True)
        return Response(serializer.data)

category_view = CategoryView.as_view()
