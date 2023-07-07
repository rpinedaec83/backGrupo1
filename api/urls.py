from django.urls import path
from . import views

urlpatterns = [
    path('api/signup/', views.signup),
    path('api/login/', views.login),
    # path('test_token', views.test_token),
    path('api/prueba/', views.prueba),
]
