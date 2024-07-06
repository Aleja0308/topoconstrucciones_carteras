from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('index/', views.index, name="index"),
    path('login/', auth_views.LoginView.as_view(template_name='layouts/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('ver_nivelacion/', views.ver_nivelacion, name='ver_nivelacion'),
    path('nivelacion/<int:nivelacion_id>/', views.crear_nivelacion, name="nivelacion"),
    path('editar_nivelacion/<int:nivelacion_id>/', views.editar_nivelacion, name='editar_nivelacion'),
    path('eliminar_nivelacion/<int:nivelacion_id>/', views.eliminar_nivelacion, name='eliminar_nivelacion'),
    path('editar_punto_nivelacion/<int:nivelacion_id>/<int:punto_id>/', views.editar_punto_nivelacion, name='editar_punto_nivelacion'),
]
