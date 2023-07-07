from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets,permissions
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer,ProductoSerializer,CategoriaSerializer
from .models import producto,categoria

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def prueba(request):
    return Response('OK')

@api_view(['POST'])
def signup(request):

    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': serializer.data})
    

    return Response(serializer.errors, status=status.HTTP_200_OK)

@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response("missing user", status=status.HTTP_404_NOT_FOUND)

    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response({'token': token.key, 'user': serializer.data})

class ProductoViewSet(viewsets.ModelViewSet):
    queryset=producto.objects.all()
    permission_classes=[permissions.AllowAny]
    serializer_class=ProductoSerializer
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset=categoria.objects.all()
    permission_classes=[permissions.AllowAny]
    serializer_class=CategoriaSerializer

@api_view(['GET'])
def ProductoFilterView(request,filter_value,value):
    if filter_value =="nombre":
        Producto=producto.objects.filter(nombre=value)
    if filter_value =="categoria":
        Producto=producto.objects.filter(categoria=value)
    if filter_value =="precio":
        Producto=producto.objects.filter(precio=value)
    serializer=ProductoSerializer(Producto,many=True)
    return Response(serializer.data)