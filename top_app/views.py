from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.contrib import messages
from .models import InformacionBasica
from .models import CarteraNivelacion
from .forms import InformacionBasicaForm
from .forms import CarteraNivelacionForm
from .forms import CarteraNivelacionFormSet

""" #LOGIN:
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
        return render(request, 'layouts/partials/login.html', {}) """

#INDEX:
#@login_required
def index(request):
    return render(request, 'layouts/index.html', {})

#CREATE Basica:
#@login_required
def add_basica(request):
    if request.method == 'POST':
        form = InformacionBasicaForm(request.POST)
        if form.is_valid():
            basica = form.save()
            return redirect('add_cartera')
    else:
        form = InformacionBasicaForm()
    return render(request, 'forms/add_basica.html', {'form': form})

#READ ver_inicio:
#@login_required
def ver_inicio(request):
    basicas = InformacionBasica.objects.all()
    return render(request, 'ver_inicio.html', {'basicas': basicas})

#READ ver_basica:
#@login_required
def ver_basica(request):
    basicas = InformacionBasica.objects.all()
    return render(request, 'ver_basica.html', {'basicas': basicas})

#UPDATE editar_basica:
#@login_required
def editar_basica(request, pk):
    basica = get_object_or_404(InformacionBasica, pk=pk)
    if request.method == 'POST':
        form = InformacionBasicaForm(request.POST, instance=basica)
        if form.is_valid():
            form.save()
            return redirect('ver_inicio')  # Redirigir a la vista 'ver_basica'
    else:
        form = InformacionBasicaForm(instance=basica)
    
    return render(request, 'forms/editar_basica.html', {'form': form, 'basica': basica})

#DELETE eliminar_basica:
#@login_required
def eliminar_basica(request, pk):
    basica = get_object_or_404(InformacionBasica, pk=pk)
    if request.method == 'POST':
        basica.delete()
        return redirect('ver_inicio')  # Redirigir a la vista 'ver_basica'
    return render(request, 'forms/eliminar_basica.html', {'basica': basica})

#CREATE CarteraNivelacion:
#@login_required
def add_cartera(request):
    if request.method == 'POST':
        form = InformacionBasicaForm(request.POST)
        formset = CarteraNivelacionFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            basica = form.save(commit=False)
            basica.save()
            formset.instance = basica
            formset.save()
            messages.success(request, 'Cartera registrada exitosamente.')
            return redirect('ver_inicio')
        else:
            if not form.is_valid():
                messages.error(request, 'Por favor corrige los errores en el formulario básico.')
            if not formset.is_valid():
                messages.error(request, 'Por favor corrige los errores en el formulario de puntos.')
    else:
        formset = CarteraNivelacionFormSet()

    # Solo pasamos el formset al contexto
    return render(request, 'forms/add_cartera.html', {'formset': formset})

#READ ver_cartera:
#@login_required
def ver_cartera(request):
    carteras = CarteraNivelacion.objects.all()
    return render(request, 'ver_cartera.html', {'carteras': carteras})

#UPDATE editar_cartera:
#@login_required
def editar_cartera(request, pk):
    cartera = get_object_or_404(CarteraNivelacion, pk=pk)
    if request.method == 'POST':
        form = CarteraNivelacionForm(request.POST, instance=cartera)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cartera actualizada exitosamente.')
            return redirect('ver_cartera')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = CarteraNivelacionForm(instance=cartera)
    
    return render(request, 'forms/editar_cartera.html', {'form': form, 'cartera': cartera})

#DELETE eliminar_cartera:
#@login_required
def eliminar_cartera(request, pk):
    cartera = get_object_or_404(CarteraNivelacion, pk=pk)
    if request.method == 'POST':
        cartera.delete()
        return redirect('ver_cartera')
    return render(request, 'forms/eliminar_cartera.html', {'cartera': cartera})

#LOGOUT:
def logout_session(request):
    logout(request)
    return redirect('login')