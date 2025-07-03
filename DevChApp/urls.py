from django.urls import path
from . import views

urlpatterns = [
    # Index
    path('', views.index, name='index'),
    # Usuario
    path('usuarios/', views.usuario_list, name='usuario_list'),
    path('usuarios/create/', views.usuario_create, name='usuario_create'),
    path('usuarios/update/<int:pk>/', views.usuario_update, name='usuario_update'),
    path('usuarios/delete/<int:pk>/', views.usuario_delete, name='usuario_delete'),

    # Vehiculo
    path('vehiculos/', views.vehiculo_list, name='vehiculo_list'),
    path('vehiculos/create/', views.vehiculo_create, name='vehiculo_create'),
    path('vehiculos/update/<int:pk>/', views.vehiculo_update, name='vehiculo_update'),
    path('vehiculos/delete/<int:pk>/', views.vehiculo_delete, name='vehiculo_delete'),

    # Ruta
    path('rutas/', views.ruta_list, name='ruta_list'),
    path('rutas/create/', views.ruta_create, name='ruta_create'),
    path('rutas/update/<int:pk>/', views.ruta_update, name='ruta_update'),
    path('rutas/delete/<int:pk>/', views.ruta_delete, name='ruta_delete'),
]
