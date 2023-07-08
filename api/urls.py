from django.urls import include, path
from . import views
from rest_framework import routers, views
from .views import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from rest_framework.response import Response

router = routers.DefaultRouter()

router.register('api/producto', ProductoViewSet , "productos")
router.register('api/pedido', PedidoViewSet , "pedidos")
router.register('api/detalle_pedido', Detalle_pedidoViewSet , "detalle_pedidos")
router.register('api/cliente', ClienteViewSet , "clientes")
router.register('api/categorias',CategoriaViewSet,'categorias')
router.register(r'api/signup', SignupViewSet, basename='signup')
router.register(r'api/login', LoginViewSet, basename='login')
# router.register('api/signup', api_view.signup)

urlpatterns = [
    path('',include(router.urls)),
    #filtrado de productos
    path('api/producto/get/<str:filter_value>/<str:value>',ProductoFilterView,name='producto_filter_view'),
    path('api/producto/get/<str:filter_value>/<str:value>',ProductoFilterView,name='producto_filter_view'),
    # path('api/signup/', views.signup),
    # path('api/login/', views.login),
    # path('test_token', views.test_token),
    # path('api/prueba/', views.prueba),

    path("api/agregar_producto_al_carrito/", csrf_exempt(agregar_producto_al_carrito), name='agregar_producto_al_carrito'),
    path("api/eliminar_producto_al_carrito/", csrf_exempt(eliminar_producto_al_carrito), name='eliminar_producto_al_carrito'),
    path("api/detalle_pedido_show/", csrf_exempt(detalle_pedido_show), name='detalle_pedido_show'),
    path("api/get_pedido_con_cupon/", csrf_exempt(get_pedido_con_cupon), name='get_pedido_con_cupon'),
]
