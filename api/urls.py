from django.urls import path
from . import views

router=routers.DefaultRouter()
router.register('api/productos',ProductoViewSet,'productos')
router.register('api/categorias',CategoriaViewSet,'categorias')
urlpatterns = [
    path('',include(router.urls)),
    #filtrado de productos
    path('api/producto/get/<str:filter_value>/<str:value>',ProductoFilterView,name='producto_filter_view'),
    path('api/producto/get/<str:filter_value>/<str:value>',ProductoFilterView,name='producto_filter_view'),
    path('api/signup/', views.signup),
    path('api/login/', views.login),
    # path('test_token', views.test_token),
    path('api/prueba/', views.prueba),
]
