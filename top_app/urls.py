from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login', auth_views.LoginView.as_view(template_name = 'layouts/login.html'), name="login"),
]
