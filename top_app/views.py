from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.http import JsonResponse, HttpResponse
from .models import InformacionBasica, CarteraNivelacion, TipoPunto, Punto, PuntoBM, PuntoDelta, PuntoCambio
from .models import CarteraNivelacion
from .forms import InformacionBasicaForm
from .forms import CarteraNivelacionForm
import json
import traceback

#LOGIN:
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
#Autenticar al usuario utilizando el nombre del usuario y el documento de identidad:
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'ver_inicio')
            return redirect(next_url)
        else:
            return render(request, 'layouts/partials/login.html', {})
    else:
        return render(request, 'layouts/partials/login.html', {})

#@login_required
def index(request):
    return render(request, 'layouts/index.html', {})

#@login_required
def ver_inicio(request):
    basicas = InformacionBasica.objects.all()
    return render(request, 'ver_inicio.html',  {'basicas': basicas})

#CREATE BASICA:
#@login_required
def add_basica(request):
    if request.method == 'POST':
        form = InformacionBasicaForm(request.POST)
        if form.is_valid():
            # Guardar el registro en la base de datos
            nueva_basica = form.save()

            # Redirigir a la vista de agregar cartera, pasando el ID de `nueva_basica`
            return redirect('add_cartera', pk=nueva_basica.id)
    else:
        form = InformacionBasicaForm()
    
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
    return render(request, 'forms/editar_basica.html', {'form': form})

#DELETE BASICA:
#@login_required
def eliminar_basica(request, pk):
    if request.method == "POST":
        basica = get_object_or_404(InformacionBasica, pk=pk)
        basica.delete()
        return JsonResponse({"success": True})
    return redirect('historial_carteras')

#CREATE CARTERA:
#@login_required
def add_cartera(request, pk):
    # Obtener el objeto de la cartera básica (InformacionBasica) relacionado
    basica = get_object_or_404(InformacionBasica, pk=pk)

    if request.method == 'POST':
        # Crear el formulario y pasarlo con los datos POST
        form = CarteraNivelacionForm(request.POST)

        if form.is_valid():
            # Obtener los datos del formulario
            tipo_punto = form.cleaned_data.get('tipo_punto')
            altura_instrumental = form.cleaned_data.get('altura_instrumental')
            vista_mas = form.cleaned_data.get('vista_mas')
            vista_menos = form.cleaned_data.get('vista_menos')
            cota = form.cleaned_data.get('cota')

            # Asignar 0.00 si los valores son vacíos
            altura_instrumental = altura_instrumental if altura_instrumental else Decimal('0.00')
            vista_mas = vista_mas if vista_mas else Decimal('0.00')
            vista_menos = vista_menos if vista_menos else Decimal('0.00')
            cota = cota if cota else Decimal('0.00')

            # Guardar el primer punto BM
            if tipo_punto == "BM":
                CarteraNivelacion.objects.create(
                    basica=basica,
                    tipo_punto=tipo_punto,
                    altura_instrumental=altura_instrumental,
                    vista_mas=vista_mas,
                    vista_menos=vista_menos,
                    cota=cota
                )

            # Guardar el tipo de punto Delta
            elif tipo_punto == "Delta":
                if cota is None or vista_menos is None:
                    form.add_error('cota', 'Para el tipo de punto Delta, la cota inicial y vista (-) son obligatorios.')
                else:
                    cota = altura_instrumental - vista_menos
                    CarteraNivelacion.objects.create(
                        basica=basica,
                        tipo_punto=tipo_punto,
                        altura_instrumental=altura_instrumental,
                        vista_mas=vista_mas,
                        vista_menos=vista_menos,
                        cota=cota
                    )

            # Guardar el tipo de punto Cambio
            elif tipo_punto == "Cambio":
                if vista_mas is None or vista_menos is None:
                    form.add_error('vista_mas', 'Para el tipo de punto Cambio, ambas vistas (+) y (-) son obligatorias.')
                else:
                    cota = altura_instrumental - vista_menos
                    altura_instrumental = cota + vista_mas
                    CarteraNivelacion.objects.create(
                        basica=basica,
                        tipo_punto=tipo_punto,
                        altura_instrumental=altura_instrumental,
                        vista_mas=vista_mas,
                        vista_menos=vista_menos,
                        cota=cota
                    )

            # Si el formulario es válido, redirigir a otra página o mostrar éxito
            return render(request, 'ver_basica.html', {'basica': basica})

    else:
        form = CarteraNivelacionForm()

    return render(request, 'forms/add_cartera.html', {'form': form, 'basica': basica})

#GUARDAR PUNTO BM

def guardar_punto_bm(request, cartera_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print(data)
            print("ID de cartera recibido:", cartera_id)
            # Crear formulario con los datos recibidos
            basica = InformacionBasica.objects.get(id=cartera_id)

            cartera = CarteraNivelacion.objects.create(
                id=basica.id,
                basica_id = basica.id
            )

            punto_bm = PuntoBM.objects.create(
                vista_mas=Decimal(data.get("vista_mas")) if data.get("vista_mas") else None,
                cota_inicial=Decimal(data.get("cota")) if data.get("cota") else None
            )

            cartera.cota = punto_bm.cota_inicial
            cartera.altura_instrumental = punto_bm.vista_mas + punto_bm.cota_inicial
            cartera.save()
            punto = Punto.objects.create(
                tipo_punto_id=1,
                punto = data.get("punto"),
                registro_id = punto_bm.id,
                cartera_nivelacion_id = cartera.id
            )

            return JsonResponse({
                "success": True,
                "message": "Punto BM guardado correctamente",
                "punto": punto.punto,
                "alturaInstrumental": cartera.altura_instrumental,
                "vistaMas": punto_bm.vista_mas,
                "cota": cartera.cota
            }, status=201)
            
        except Exception as e:
            print("Error:", e)  # Imprimir el error en la terminal
            print("Traceback:", traceback.format_exc())  # Ver detalles del error
            return JsonResponse({
                "success": False,
                "message": str(e) + "\n" + traceback.format_exc()
            }, status=500)
    return JsonResponse({"success": False, "message": "Método no permitido"}, status=405)


#GUARDAR PUNTO DELTA
def guardar_punto_delta(request, cartera_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            cartera = CarteraNivelacion.objects.get(id=cartera_id)

            punto_delta = PuntoDelta.objects.create(
                vista_menos=Decimal(data.get("vista_menos")) if data.get("vista_menos") else None,
            )

            cartera.cota = cartera.altura_instrumental - punto_delta.vista_menos
            cartera.save()
            punto = Punto.objects.create(
                tipo_punto_id=2,
                punto = data.get("punto"),
                registro_id = punto_delta.id,
                cartera_nivelacion_id = cartera.id
            )

            return JsonResponse({
                "success": True,
                "message": "Punto Delta guardado correctamente",
                "punto": punto.punto,
                "alturaInstrumental": cartera.altura_instrumental,
                "vistaMenos": punto_delta.vista_menos,
                "cota": cartera.cota
            }, status=201)
            
        except Exception as e:
            print("Error:", e)  # Imprimir el error en la terminal
            print("Traceback:", traceback.format_exc())  # Ver detalles del error
            return JsonResponse({
                "success": False,
                "message": str(e) + "\n" + traceback.format_exc()
            }, status=500)
    return JsonResponse({"success": False, "message": "Método no permitido"}, status=405)

#GUARDAR PUNTO CAMBIO
def guardar_punto_cambio(request, cartera_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            cartera = CarteraNivelacion.objects.get(id=cartera_id)
            punto_cambio = PuntoCambio.objects.create(
                vista_mas=Decimal(data.get("vista_mas")) if data.get("vista_mas") else None,
                vista_menos=Decimal(data.get("vista_menos")) if data.get("vista_menos") else None,
            )

            cartera.cota = cartera.altura_instrumental - punto_cambio.vista_menos
            cartera.altura_instrumental = cartera.cota + punto_cambio.vista_mas
            cartera.save()

            punto = Punto.objects.create(
                tipo_punto_id=3,
                punto = data.get("punto"),
                registro_id = punto_cambio.id,
                cartera_nivelacion_id = cartera.id
            )

            return JsonResponse({
                "success": True,
                "message": "Punto Cambio guardado correctamente",
                "punto": punto.punto,
                "alturaInstrumental": cartera.altura_instrumental,
                "vistaMas": punto_cambio.vista_mas,
                "vistaMenos": punto_cambio.vista_menos,
                "cota": cartera.cota
            }, status=201)
            
        except Exception as e:
            print("Error:", e)  # Imprimir el error en la terminal
            print("Traceback:", traceback.format_exc())  # Ver detalles del error
            return JsonResponse({
                "success": False,
                "message": str(e) + "\n" + traceback.format_exc()
            }, status=500)
    return JsonResponse({"success": False, "message": "Método no permitido"}, status=405)

#READ CARTERA:
#@login_required
def ver_cartera(request, pk):
    cartera = CarteraNivelacion.objects.filter(basica_id=pk)
    basica = InformacionBasica.objects.get(pk=pk)
    return render(request, 'ver_cartera.html', {'carteras': cartera, 'basica': basica})

#UPDATE CARTERA:
#@login_required
def editar_cartera(request, pk):
    # Asegúrate de obtener el objeto correctamente
    cartera = get_object_or_404(CarteraNivelacion, pk=pk)

    if request.method == "POST":
        form = CarteraNivelacionForm(request.POST, instance=cartera)
        if form.is_valid():
            cartera = form.save(commit=False)
            cartera.calcular_cota()
            cartera.save()
            # Asegúrate de redirigir con el pk correcto
            return redirect('ver_cartera', pk=cartera.pk)
    else:
        form = CarteraNivelacionForm(instance=cartera)

    return render(request, 'forms/editar_cartera.html', {'form': form, 'cartera': cartera})

#DELETE CARTERA:
#@login_required
def eliminar_cartera(request, pk):
    if request.method == 'POST':  # Verifica que sea una solicitud POST
        cartera = get_object_or_404(CarteraNivelacion, pk=pk)  # Obtén el objeto o devuelve 404
        cartera.delete()  # Elimina el objeto
        return JsonResponse({'success': True})  # Devuelve una respuesta JSON de éxito
    return JsonResponse({'error': 'Método no permitido'}, status=405)  # Si no es POST, responde con error

#LOGOUT:
#@login_required
def logout_session(request):
    logout(request)
    return redirect('login')