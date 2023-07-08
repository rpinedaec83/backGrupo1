from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id', 'username', 'password', 'email']

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'


class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'


class Detalle_pedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detalle_pedido
        fields = '__all__'

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields='__all__'

class DetalleCompraSerializer(serializers.ModelSerializer):
    producto = serializers.CharField(source='producto.nombre')

    class Meta:
        model = Detalle_pedido
        fields = ('id', 'producto', 'cantidad', 'subtotal')

class CompraSerializer(serializers.ModelSerializer):
    detalles_pedido = DetalleCompraSerializer(many=True, read_only=True)
    cliente = serializers.CharField(source='cliente.username')
    estado = serializers.CharField(source='estado.descripcion')
    cupon = serializers.CharField(source='cupon.descripcion', allow_null=True)

    class Meta:
        model = Pedido
        fields = ('id', 'fecha', 'subtotal', 'igv', 'total', 'cliente', 'estado', 'cupon', 'detalles_pedido')
