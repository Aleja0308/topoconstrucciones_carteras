from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
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
          basica_instance = form.save(commit=False)
          basica_instance.save()
          return redirect('add_cartera', basica_id=basica_instance.id)
    else:
        form = InformacionBasicaForm()  #Se crea un formulario vacío para solicitudes GET
    return render(request, 'forms/basica.html', {'form': form})

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
            return redirect('ver_basica')  # Redirigir a la vista 'ver_basica'
    else:
        form = InformacionBasicaForm(instance=basica)
    
    return render(request, 'forms/editar_basica.html', {'form': form, 'basica': basica})

#DELETE eliminar_basica:
#@login_required
def eliminar_basica(request, pk):
    basica = get_object_or_404(InformacionBasica, pk=pk)
    if request.method == 'POST':
        basica.delete()
        return redirect('ver_basica')  # Redirigir a la vista 'ver_basica'
    return render(request, 'forms/eliminar_basica.html', {'basica': basica})

#CREATE CarteraNivelacion:
#@login_required
def add_cartera(request, basica_id=None):
    basica_instance = get_object_or_404(InformacionBasica, pk=basica_id)
    
    if request.method == 'POST':
        formset = CarteraNivelacionForm(request.POST)
        if formset.is_valid():
            cartera_instances = formset.save(commit=False)
            cota_inicial = basica_instance.cota_inicial
            vista_mas = basica_instance.vista_mas
            
            for instance in cartera_instances:
                instance.basica = basica_instance
                tipo_punto = instance.tipo_punto
                altura_instrumental = vista_mas + cota_inicial
    
                if tipo_punto == 'Delta':
                    vista_menos = instance.vista_menos
                    instance.cota_calculada = altura_instrumental - vista_menos
    
                elif tipo_punto == 'Cambio':
                    vista_mas = instance.vista_mas
                    vista_menos = instance.vista_menos
                    cota_calculada = altura_instrumental - vista_menos
                    instance.altura_instrumental = cota_calculada + vista_mas
 
                instance.save() #Guarda cada instancia.
                
            return redirect('ver_inicio')  # Redirigir a la vista 'ver_inicio'
    else:
        formset = CarteraNivelacionForm()
    
    return render(request, 'forms/cartera.html', {'formset': formset, 'basica_id': basica_id})


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
            return redirect('ver_cartera')  # Redirigir a la vista 'ver_cartera'
    else:
        form = CarteraNivelacionForm(instance=cartera)
    
    return render(request, 'forms/editar_cartera.html', {'form': form, 'cartera': cartera})

#DELETE editar_cartera:
#@login_required
def eliminar_cartera(request, pk):
    cartera = get_object_or_404(CarteraNivelacion, pk=pk)
    if request.method == 'POST':
        cartera.delete()
        return redirect('ver_cartera')  # Redirigir a la vista 'ver_cartera'
    return render(request, 'forms/eliminar_cartera.html', {'cartera': cartera})

#LOGOUT:
def logout_session(request):
    logout(request)
    return redirect('login')