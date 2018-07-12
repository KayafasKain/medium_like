from django.apps import apps

from django.contrib.auth import (
    get_user_model,
)

from .serializers import PostSerializer, StatusSerializer, CategotySerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

PostArticle = apps.get_model('post_app', 'PostArticle')
Status = apps.get_model('post_app', 'Status')
Categoty = apps.get_model('post_app', 'Category')

class PostViewSet(viewsets.ModelViewSet):
    queryset = PostArticle.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if self.request.user.is_staff:
            self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Categoty.objects.all()
    serializer_class = CategotySerializer

class StatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
