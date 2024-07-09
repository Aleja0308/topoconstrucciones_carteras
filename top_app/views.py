from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Basica, CarteraNivelacion
from .forms import BasicaForm, TipoPuntoForm, CarteraNivelacionForm

#LOGIN:
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
#Autenticar al usuario utilizando el nombre del usuario y el documento de identidad:
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('ver_inicio')
        else:
            return redirect('login')
    else:
        return render(request, 'layouts/partials/login.html', {})

#INDEX:
@login_required
def index(request):
    return render(request, 'layouts/index.html', {})

#CREATE TipoPunto:
@login_required
def add_tipo(request):
    if request.method == 'POST':
        form = TipoPuntoForm(request.POST)
        if form.is_valid():
            tipo_punto = form.save()
            return render(request, 'options/tipo_punto.html', {'tipo_punto': tipo_punto})
    else:
        form = TipoPuntoForm()
    return render(request, 'options/tipo_punto.html', {'form': form})

#CREATE Basica:
@login_required
def add_basica(request):
    if request.method == 'POST':
        form = BasicaForm(request.POST)
        if form.is_valid():
            basica_instance = form.save(commit=False)
            basica_instance.save()
            return redirect('add_cartera', basica_id=basica_instance.id)
    else:
        form = BasicaForm()
    return render(request, 'forms/basica.html', {'form': form})

#READ ver_inicio:
@login_required
def ver_inicio(request):
    basicas = Basica.objects.all()
    return render(request, 'ver_inicio.html', {'basicas': basicas})

#READ ver_basica:
@login_required
def ver_basica(request):
    basicas = Basica.objects.all()
    return render(request, 'ver_basica.html', {'basicas': basicas})

#UPDATE editar_basica:
@login_required
def editar_basica(request, pk):
    basica = get_object_or_404(Basica, pk=pk)
    if request.method == 'POST':
      form = BasicaForm(request.POST, instance=basica)
      if form.is_valid():
        form.save()
        return redirect('editar_basica')
    else:
        form = BasicaForm(instance=basica)
    return render(request, 'forms/editar_basica.html', {'form': form, 'basica': basica})

#DELETE eliminar_basica:
@login_required
def eliminar_basica(request, pk):
    basica = get_object_or_404(Basica, pk=pk)
    if request.method == 'POST':
        basica.delete()
        return redirect('ver_basica')
    return render(request, 'forms/eliminar_basica.html', {'basica': basica})

#CREATE CarteraNivelacion:
@login_required
def add_cartera(request, basica_id=None):
    basica_instance = Basica.objects.get(pk=basica_id)
    if request.method == 'POST':
        form = CarteraNivelacionForm(request.POST)
        if form.is_valid():
            cartera_instance = form.save(commit=False)
            cartera_instance.basica = basica_instance
            cartera_instance.save()
            return redirect('ver_inicio')
    else:
        form = CarteraNivelacionForm()
    return render(request, 'forms/cartera.html', {'form': form, 'basica_id': basica_id})

#READ ver_cartera:
@login_required
def ver_cartera(request):
    carteras = CarteraNivelacion.objects.all()
    return render(request, 'ver_cartera.html', {'carteras': carteras})

#UPDATE editar_cartera:
@login_required
def editar_cartera(request, pk):
    cartera = get_object_or_404(CarteraNivelacion, pk=pk)
    if request.method == 'POST':
      form = CarteraNivelacionForm(request.POST, instance=cartera)
      if form.is_valid():
          form.save()
          return redirect('ver_inicio')
    else:
        form = CarteraNivelacionForm(instance=cartera)
    return render(request, 'forms/editar_cartera.html', {'form': form, 'cartera': cartera})

#DELETE editar_cartera:
@login_required
def eliminar_cartera(request, pk):
    cartera = get_object_or_404(CarteraNivelacion, pk=pk)
    if request.method == 'POST':
        cartera.delete()
        return redirect('ver_cartera')
    return render(request, 'forms/eliminar_cartera', {'cartera': cartera})

#LOGOUT:
def logout_session(request):
    logout(request)
    return redirect('login')