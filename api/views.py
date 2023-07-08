from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets,permissions
from rest_framework import status
from rest_framework import generics
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from .serializers import *
from .models import *
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from django.http import Http404



class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ProductoSerializer

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = PedidoSerializer

class Detalle_pedidoViewSet(viewsets.ModelViewSet):
    queryset = Detalle_pedido.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = Detalle_pedidoSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ClienteSerializer
   
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset=Categoria.objects.all()
    permission_classes=[permissions.AllowAny]
    serializer_class=CategoriaSerializer


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


def agregar_producto_al_carrito(request):

    if(request.method == 'POST'):
        print(request.POST.get('cliente_id')) 
        print(request.POST.get('producto_id')) 

        try:
            cliente_ = get_object_or_404(Cliente, id= request.POST.get('cliente_id'))
            producto_ = get_object_or_404(Producto, id=request.POST.get('producto_id'))

            estado_ = Estado_pedido.objects.get(descripcion="enCarrito")
            pedido_ = Pedido.objects.get_or_create(#devuelve una tupla por eso se accede por conchetes
                cliente= cliente_,
                estado= estado_, 
                defaults={
                    'subtotal': 0,
                    'igv': 18,
                    'total': 0,
                    'cupon': None,
            })

            pedido_[0].total = pedido_[0].total + producto_.precio - producto_.descuento
            pedido_[0].save()

            new_detalle = Detalle_pedido(pedido=pedido_[0], producto=producto_, cantidad=1, subtotal=producto_.precio*1)
            new_detalle.save()

        except Http404 as error_:
            print(str(error_))


        return HttpResponse("Se agregó con éxito")


def eliminar_producto_al_carrito(request):
    
    if(request.method == 'POST'):

        producto_ = get_object_or_404(Producto, id=request.POST.get('producto_id'))
        cliente_ = get_object_or_404(Cliente, id=request.POST.get('cliente_id'))#si no lo encuentra tira 440
        pedido_ = get_object_or_404(Pedido, cliente=cliente_)

        detalle_  = Detalle_pedido.objects.filter(pedido=pedido_,producto=producto_)

        pedido_.total -= producto_.precio
        pedido_.save()
        detalle_.delete()

        return HttpResponse("Se eliminó con éxito")
        #return render(request, "otro.html")


def detalle_pedido_show(request):
    
    if(request.method == 'POST'):
        pedido_ = get_object_or_404(Pedido, cliente=request.POST.get('cliente_id'))
        detalle_pedidos_ = Detalle_pedido.objects.filter(pedido=pedido_)

        costo_total = 0
        for pedido in detalle_pedidos_:
            costo_total += pedido.producto.precio
            costo_total -= pedido.producto.descuento

        return render(request, 'detalle_pedido_show.html',  {'detalle_pedidos_':detalle_pedidos_, 'costo_total': costo_total})


def get_pedido_con_cupon(request):
    
    if(request.method == 'POST'):

        pedido_ = get_object_or_404(Pedido, id=request.POST.get('pedido_id'))
        cupon_ = get_object_or_404(Cupon, codigo=request.POST.get('codigo_'))

        nuevo_costo = pedido_.total - cupon_.descuento
        detalle_pedidos_ = Detalle_pedido.objects.filter(pedido=pedido_)


        return render(request, 'detalle_pedido_show.html',  {'detalle_pedidos_':detalle_pedidos_, 'costo_total': nuevo_costo})


@api_view(['GET'])
def ProductoFilterView(request,filter_value,value):
    if filter_value =="nombre":
        producto=Producto.objects.filter(nombre=value)
    if filter_value =="categoria":
        producto=Producto.objects.filter(categoria=value)
    if filter_value =="precio":
        producto=Producto.objects.filter(precio=value)
    serializer=ProductoSerializer(producto,many=True)
    return Response(serializer.data)

class MisComprasAPIView(generics.RetrieveAPIView):
    serializer_class = CompraSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Pedido.objects.filter(cliente_id=pk)

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response_data = serializer.data
        detalle_compra_data = []
        for detalle in instance.detalle_pedido_set.all():
            detalle_serializer = DetalleCompraSerializer(detalle)
            detalle_compra_data.append(detalle_serializer.data)
        response_data['detalle_pedido'] = detalle_compra_data
        return Response(response_data)