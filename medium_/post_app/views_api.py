from django.apps import apps
from django.contrib.auth import (
    get_user_model,
)
from django.http import Http404
from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .permission import IsOwnerOrReadOnly, IsStaffOrReadOnly
from .serializers import PostSerializer, StatusSerializer, CategotySerializer

PostArticle = apps.get_model('post_app', 'PostArticle')
Status = apps.get_model('post_app', 'Status')
Categoty = apps.get_model('post_app', 'Category')

class PostViewSet(viewsets.ModelViewSet):
    queryset = PostArticle.objects.all().order_by('-pk')
    serializer_class = PostSerializer
    permission_classes = (IsStaffOrReadOnly, IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Categoty.objects.all()
    serializer_class = CategotySerializer
    permission_classes = (IsStaffOrReadOnly,)

class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = (IsStaffOrReadOnly,)
