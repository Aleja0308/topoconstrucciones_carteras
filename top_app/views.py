from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from .models import InformacionBasica
from .models import CarteraNivelacion
from .forms import InformacionBasicaForm
from .forms import CarteraNivelacionForm

""" #LOGIN:
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
#Autenticar al usuario utilizando el nombre del usuario y el documento de identidad:
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('ver_inicio')
        else:
            return redirect('login')
    else:
        return render(request, 'layouts/partials/login.html', {}) """

#@login_required
def index(request):
    return render(request, 'layouts/index.html', {})

#@login_required
def ver_inicio(request):
    basicas = InformacionBasica.objects.all()
    return render(request, 'ver_inicio.html', {'basicas': basicas})

#CREATE BASICA:
#@login_required
def add_basica(request):
    if request.method == "POST":
        form = InformacionBasicaForm(request.POST)
        if form.is_valid():
          basica_instance = form.save(commit=False)
          basica_instance.save()
          return redirect('add_cartera', basica_id=basica_instance.id)
    else:
        form = InformacionBasicaForm() #Se crea un formulario vacío para solicitudes GET
    return render(request, 'forms/add_basica.html', {'form': form})
  
#READ BASICA:
#@login_required
def ver_basica(request):
    basicas = InformacionBasica.objects.all()
    return render(request, 'ver_basica.html', {'basicas': basicas})

#UPDATE BASICA:
#@login_required
def editar_basica(request, pk):
    basica = get_object_or_404(InformacionBasica, pk=pk)
    if request.method == "POST":
        form = InformacionBasicaForm(request.POST, instance=basica)
        if form.is_valid():
            form.save()
            return redirect('ver_inicio')
    else:
        form = InformacionBasicaForm(instance=basica)
    return render(request, 'forms/editar_basica.html', {'form': form, 'basica': basica})

#DELETE BASICA:
#@login_required
def eliminar_basica(request, pk):
    basica = get_object_or_404(InformacionBasica, pk=pk)
    if request.method == "POST":
        basica.delete()
        return redirect('ver_inicio')
    return render(request, 'forms/eliminar_basica.html', {'basica': basica})

#CREATE CARTERA:
#@login_required
def add_cartera(request, basica_id):
    basica = get_object_or_404(InformacionBasica, pk=basica_id)
    CarteraNivelacionFormSet = formset_factory(CarteraNivelacionForm, extra=1)
    if request.method == "POST":
        formset = CarteraNivelacionFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                cartera = form.save(commit=False)
                cartera.basica = basica
                cartera.calcular_cota()
                cartera.save()
            return redirect('ver_inicio', pk=basica.pk)
    else:
        formset = CarteraNivelacionFormSet()
    return render(request, 'forms/add_cartera.html', {'formset': formset, 'basica': basica})

#READ CARTERA:
#@login_required
def ver_cartera(request, pk):
    basica = get_object_or_404(InformacionBasica, pk=pk)
    carteras = basica.carteras.all()
    return render(request, 'ver_cartera.html', {'basica': basica, 'carteras': carteras})

#UPDATE CARTERA:
#@login_required
def editar_cartera(request, pk):
    cartera = get_object_or_404(CarteraNivelacion, pk=pk)
    if request.method == "POST":
        form = CarteraNivelacionForm(request.POST, instance=cartera)
        if form.is_valid():
            cartera = form.save(commit=False)
            cartera.calcular_cota()
            cartera.save()
            return redirect('ver_cartera', pk=cartera.basica.pk) 
    else:
        form = CarteraNivelacionForm(instance=cartera)
    return render(request, 'forms/editar_cartera.html', {'form': form})

#DELETE CARTERA:
#@login_required
def eliminar_cartera(request, pk):
    cartera = get_object_or_404(CarteraNivelacion, pk=pk)
    if request.method == "POST":
        basica_pk = cartera.basica.pk
        cartera.delete()
        return redirect('ver_inicio', pk=basica_pk)
    return render(request, 'forms/eliminar_cartera.html', {'cartera': cartera})

#LOGOUT:
#@login_required
def logout_session(request):
    logout(request)
    return redirect('login')