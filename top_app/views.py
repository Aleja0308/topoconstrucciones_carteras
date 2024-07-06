from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import TablaNivelacion, Punto
from .forms import PuntoForm

# Create your views here.

#LOGIN:
def login(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    #Autenticar al usuario utilizando el nombre del usuario y el documento de identidad:
    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)
      return redirect('ver_nivelacion')
    else:
      return redirect('login')
  else:
    return render(request, 'layouts/login.html', {})

#INDEX:  
def index(request):
  return render(request, 'layouts/index.html', {})

#FUNCIÓN PARA CREAR UNA CARTERA:
@login_required
def crear_nivelacion(request):
  if request.method == 'POST':
    nombre = request.POST.get('nombre')
    nivelacion = TablaNivelacion.objects.create(nombre=nombre)
    return redirect('editar_nivelacion', nivelacion_id=nivelacion.id)
  return render(request, 'forms/nivelacion.html')

#FUNCIÓN PARA EDITAR LA CARTERA:
@login_required
def editar_nivelacion(request, nivelacion_id):
    nivelacion = get_object_or_404(TablaNivelacion, id=nivelacion_id)
    if request.method == 'POST':
        form = PuntoForm(request.POST)
        if form.is_valid():
            punto = form.save(commit=False)
            punto.tabla = nivelacion  # Cambiado de nivelacion a tabla
            # Calcula la cota y la altura instrumental
            if punto.tipo == 'delta':
                punto.cota = punto.vista_mas
                punto.altura_instrumental = punto.cota + punto.vista_mas
            elif punto.tipo == 'cambio':
                ultimo_punto = nivelacion.puntos.last()
                if ultimo_punto:
                    punto.cota = ultimo_punto.cota - punto.vista_menos
                    punto.altura_instrumental = punto.cota + punto.vista_mas
            punto.save()
            return redirect('editar_nivelacion', nivelacion_id=nivelacion.id)
    else:
        form = PuntoForm()
    return render(request, 'forms/editar_nivelacion.html', {'nivelacion': nivelacion, 'form': form})


#FUNCIÓN PARA VISUALIZAR UN PUNTO:
@login_required
def ver_nivelacion(request, nivelacion_id):
  nivelacion = get_object_or_404(TablaNivelacion, id=nivelacion_id)
  return render(request, 'forms/ver_nivelacion.html', {'nivelacion': nivelacion})

#FUNCIÓN PARA ELIMINAR UN PUNTO:
@login_required
def eliminar_nivelacion(request, nivelacion_id):
  nivelacion = get_object_or_404(TablaNivelacion, id=nivelacion_id)
  nivelacion.delete()
  return render('listar_tablas')

#FUNCIÓN PARA EDITAR UN PUNTO:
@login_required
def editar_punto_nivelacion(request, nivelacion_id, punto_id):
    nivelacion = get_object_or_404(TablaNivelacion, id=nivelacion_id)
    punto = get_object_or_404(Punto, id=punto_id)
    
    if request.method == 'POST':
        form = PuntoForm(request.POST, instance=punto)
        if form.is_valid():
            punto = form.save(commit=False)
            # Realiza los cálculos necesarios según el tipo de punto si se actualizan las vistas
            punto.save()
            return redirect('editar_nivelacion', nivelacion_id=nivelacion_id)
    else:
        form = PuntoForm(instance=punto)
    
    return render(request, 'forms/editar_punto_nivelacion.html', {'nivelacion': nivelacion, 'form': form, 'punto': punto})

#LOGOUT:
def logout_session(request):
  logout(request)
  return redirect('login')