from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('index/', views.index, name="index"),
    path('login/', auth_views.LoginView.as_view(template_name='layouts/login.html'), name="login"),
    path('ver_inicio/', views.ver_inicio, name="ver_inicio"),
    path('add_basica/', views.add_basica, name="add_basica"),
    path('ver_basica/', views.ver_basica, name='ver_basica'),
    path('editar_basica/<int:pk>/', views.editar_basica, name='editar_basica'),
    path('eliminar_basica/<int:pk>/', views.eliminar_basica, name='eliminar_basica'),
    path('add_cartera/<int:basica_id>/', views.add_cartera, name='add_cartera'),
    path('ver_cartera/', views.ver_cartera, name='ver_cartera'),
    path('editar_cartera/<int:pk>/', views.editar_cartera, name='editar_cartera'),
    path('eliminar_cartera/<int:pk>/', views.eliminar_cartera, name='eliminar_cartera'),
    path('logout_session/', views.logout_session, name='logout_session'),
]