from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id', 'username', 'password', 'email']
from .models import producto,categoria

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = producto
        fields='__all__'
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = categoria
        fields='__all__'