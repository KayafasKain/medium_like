from django.contrib.auth import (
    get_user_model,
)

from .serializers import UserSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


User = get_user_model()
class UserList(APIView):
    context_object_name = 'api-user-list'
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

user_list = UserList.as_view()
