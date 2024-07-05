from django.shortcuts import render, get_object_or_404, redirect
from .models import TablaNivelacion, Punto
from .forms import PuntoForm

# Create your views here.

#Función para crear la tabla:
def crear_nivelacion(request):
  if request.method == 'POST':
    nombre = request.POST.get('nombre')
    nivelacion = TablaNivelacion.objects.create(nombre=nombre)
    return redirect('editar_nivelacion', nivelacion_id=nivelacion.id)
  return render(request, 'forms/nivelacion.html')

#Función para editar la tabla:
def editar_nivelacion(request, nivelacion_id):
  nivelacion = get_object_or_404(TablaNivelacion, id = nivelacion_id)
  if request.method == 'POST':
    form = PuntoForm(request.POST)
    if form.is_valid():
      punto = form.save(commit=False)
      punto.nivelacion = nivelacion
      #Calcula la cota y la altura instrumenta
      if punto.tipo == 'delta':
        punto.cota = punto.vista_mas
        punto.altura_instrumental = punto.cota + punto.vista_mas
      elif punto.tipo == 'cambio':
        punto.cota =nivelacion.puntos.last().cota - punto.vista_menos
        punto.altura_instrumental = punto.cota + punto.vista_mas
      punto.save()
      return redirect('editar_nivelacion', nivelacion_id = nivelacion_id)
  else:
    form = PuntoForm()
  return render(request, 'forms/editar_nivelacion.html', {'nivelacion': nivelacion, 'form': form})

#Función para visualizar la tabla:
def ver_nivelacion(request, nivelacion_id):
  nivelacion = get_object_or_404(TablaNivelacion, id=nivelacion_id)
  return render(request, 'forms/ver_nivelacion.html', {'nivelacion': nivelacion})

#Función para eliminar la tabla:
def eliminar_nivelacion(request, nivelacion_id):
  nivelacion = get_object_or_404(TablaNivelacion, id=nivelacion_id)
  nivelacion.delete()
  return render('listar_tablas')

#Función para editar un punto de manera individual:
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