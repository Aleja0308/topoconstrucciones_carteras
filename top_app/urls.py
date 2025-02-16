from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('index/', views.index, name="index"),
    path('', auth_views.LoginView.as_view(template_name='layouts/login.html'), name="login"),
    path('ver_inicio/', views.ver_inicio, name='ver_inicio'),
    path('add_basica/', views.add_basica, name="add_basica"),
    path('ver_basica/', views.ver_basica, name='ver_basica'),
    path('editar_basica/<int:pk>/', views.editar_basica, name='editar_basica'),
    path('eliminar_basica/<int:pk>/', views.eliminar_basica, name='eliminar_basica'),
    path('add_cartera/<int:pk>/', views.add_cartera, name='add_cartera'),
    path('guardar-punto-bm/<int:cartera_id>/', views.guardar_punto_bm, name='guardar_punto_bm'),
    path('guardar-punto-delta/<int:cartera_id>/', views.guardar_punto_delta, name='guardar_punto_delta'),
    path('guardar-punto-cambio/<int:cartera_id>/', views.guardar_punto_cambio, name='guardar_punto_cambio'),
    path('ver_cartera/<int:pk>/', views.ver_cartera, name='ver_cartera'),
    path('editar_cartera_template/<int:pk>/', views.editar_cartera_template, name='editar_cartera_template'),
    path('editar_punto/<int:punto_id>/', views.editar_punto, name='editar_punto'),
    path('eliminar_punto/<int:pk>/', views.eliminar_punto, name='eliminar_punto'),
    path('logout_session/', views.logout_session, name="logout_session"),
]