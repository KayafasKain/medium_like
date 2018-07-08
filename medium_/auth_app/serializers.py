from rest_framework import serializers
from django.contrib.auth import (
    get_user_model,
)

User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'last_login',
            'username',
            'first_name',
            'last_name',
            'email'
        )
