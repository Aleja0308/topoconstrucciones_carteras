from decimal import Decimal, InvalidOperation
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.http import JsonResponse, HttpResponse
from .models import InformacionBasica, CarteraNivelacion, Puntos
from .models import CarteraNivelacion
from .forms import InformacionBasicaForm
from .forms import CarteraNivelacionForm
from .forms import PuntosForm
from django.db import transaction
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

@login_required
def index(request):
    return render(request, 'layouts/index.html', {})

@login_required
def ver_inicio(request):
    basicas = InformacionBasica.objects.all()
    return render(request, 'ver_inicio.html',  {'basicas': basicas})

#CREATE BASICA:
@login_required
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
@login_required
def ver_basica(request):
    basicas = InformacionBasica.objects.all()
    return render(request, 'ver_basica.html', {'basicas': basicas})

#UPDATE BASICA:
@login_required
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
@login_required
def eliminar_basica(request, pk):
    if request.method == "POST":
        basica = get_object_or_404(InformacionBasica, pk=pk)
        basica.delete()
        return JsonResponse({"success": True})
    return redirect('historial_carteras')

#CREATE CARTERA:
@login_required
def add_cartera(request, pk):
    # Obtener el objeto de la cartera básica (InformacionBasica) relacionado
    basica = get_object_or_404(InformacionBasica, pk=pk)

    cartera, created = CarteraNivelacion.objects.get_or_create(
        id=basica.id,
        defaults={"basica_id": basica.id}
    )

    return render(request, 'forms/add_cartera.html', {'cartera': cartera})

#GUARDAR PUNTO BM

def guardar_punto_bm(request, cartera_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print(data)
            print("ID de cartera recibido:", cartera_id)

            # Intentar convertir vista_mas y cota_inicial a Decimal
            try:
                vista_mas = Decimal(data.get("vista_mas") or 0)
            except InvalidOperation:
                return JsonResponse({
                    "success": False,
                    "message": "Error: Vista (+) no tiene un formato válido."
                }, status=400)
            try:
                cota_inicial = Decimal(data.get("cota") or 0)
            except InvalidOperation:
                return JsonResponse({
                    "success": False,
                    "message": "Error: Cota no tiene un formato válido."
                }, status=400)
            
            if (vista_mas<=0):
                return JsonResponse({
                    "success": False,
                    "message": "Error: Vista(+) debe ser positiva."
                }, status=400)
            
            if (cota_inicial<=0):
                return JsonResponse({
                    "success": False,
                    "message": "Error: Cota debe ser positiva."
                }, status=400)

            # Obtener la información básica
            basica = InformacionBasica.objects.get(id=cartera_id)

            # Verificar si ya existe una cartera de nivelación
            cartera, created = CarteraNivelacion.objects.get_or_create(
                id=basica.id,
                defaults={"basica_id": basica.id}
            )

            # Verificar si la cartera ya tiene un punto BM
            existe_punto_bm = Puntos.objects.filter(
                cartera_nivelacion_id=cartera.id, tipo_punto_id=1
            ).exists()
            
            if existe_punto_bm:
                return JsonResponse({
                    "success": False,
                    "message": "Error: La cartera ya tiene un punto de tipo BM."
                }, status=400)


            # Actualizar valores en la cartera y guardar
            cartera.cota = cota_inicial
            cartera.altura_instrumental = vista_mas + cota_inicial
            cartera.save()

            # Crear punto BM
            punto_bm = Puntos.objects.create(
                tipo_punto_id=1,
                punto=data.get("punto"),
                cartera_nivelacion_id=cartera.id,
                vista_mas=vista_mas,
                cota=cota_inicial,
                altura_instrumental = cartera.altura_instrumental
            )

            return JsonResponse({
                "success": True,
                "message": "Punto BM guardado correctamente",
                "punto": punto_bm.punto,
                "alturaInstrumental": cartera.altura_instrumental,
                "vistaMas": punto_bm.vista_mas,
                "cota": cartera.cota
            }, status=201)

        except InformacionBasica.DoesNotExist:
            return JsonResponse({
                "success": False,
                "message": "Error: No se encontró la información básica con el ID proporcionado."
            }, status=404)

        except Exception as e:
            print("Error:", e)  # Imprimir el error en la terminal
            print("Traceback:", traceback.format_exc())  # Ver detalles del error
            return JsonResponse({
                "success": False,
                "message": f"Error inesperado: {str(e)}",
                "traceback": traceback.format_exc()
            }, status=500)

    return JsonResponse({"success": False, "message": "Método no permitido"}, status=405)


#GUARDAR PUNTO DELTA
def guardar_punto_delta(request, cartera_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            try:
                vista_menos = Decimal(data.get("vista_menos") or 0)
            except InvalidOperation:
                return JsonResponse({
                    "success": False,
                    "message": "Error: Vista (-) no tiene un formato válido."
                }, status=400)

            if (vista_menos<=0):
                return JsonResponse({
                    "success": False,
                    "message": "Error: Vista(-) debe ser positiva."
                }, status=400)

            cartera = CarteraNivelacion.objects.get(id=cartera_id)

            nueva_cota = cartera.altura_instrumental - vista_menos

            if (nueva_cota<=0): 
                return JsonResponse({
                    "success": False,
                    "message": "Error: Vista (-) no válida. La cota calculada debe ser superior a 0."
                }, status=400)
            
            punto_delta = Puntos.objects.create(
                tipo_punto_id=2,
                punto=data.get("punto"),
                altura_instrumental = cartera.altura_instrumental,
                vista_menos=vista_menos,
                cota = nueva_cota,
                cartera_nivelacion_id=cartera.id
            )


            cartera.cota = nueva_cota
            cartera.save()
        

            return JsonResponse({
                "success": True,
                "message": "Punto Delta guardado correctamente",
                "punto": punto_delta.punto,
                "alturaInstrumental": cartera.altura_instrumental,
                "vistaMenos": punto_delta.vista_menos,
                "cota": cartera.cota
            }, status=201)
            
        except CarteraNivelacion.DoesNotExist:
            return JsonResponse({
                "success": False,
                "message": "Error: No se encontró la cartera nivelación con el ID proporcionado."
            }, status=404)
        
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
            try:
                vista_mas = Decimal(data.get("vista_mas") or 0)
            except InvalidOperation:
                return JsonResponse({
                    "success": False,
                    "message": "Error: Vista (+) no tiene un formato válido."
                }, status=400)

            if (vista_mas<=0):
                return JsonResponse({
                    "success": False,
                    "message": "Error: Vista(+) no puede ser negativa."
                }, status=400)
            try:
                vista_menos = Decimal(data.get("vista_menos") or 0)
            except InvalidOperation:
                return JsonResponse({
                    "success": False,
                    "message": "Error: Vista (-) no tiene un formato válido."
                }, status=400)

            if (vista_menos<=0):
                return JsonResponse({
                    "success": False,
                    "message": "Error: Vista(-) no puede ser negativa."
                }, status=400)
            

            cartera = CarteraNivelacion.objects.get(id=cartera_id)

            nueva_cota = cartera.altura_instrumental - vista_menos
            if (nueva_cota<=0):
                return JsonResponse({
                    "success": False,
                    "message": "Error: Vista (-) no válida. La cota calculada debe ser mayor a 0."
                }, status=400)
            
            nueva_altura_instrumental = nueva_cota + vista_mas

            punto_cambio = Puntos.objects.create(
                tipo_punto_id=3,
                punto=data.get("punto"),
                altura_instrumental = nueva_altura_instrumental,
                vista_mas=vista_mas,
                vista_menos=vista_menos,
                cota = nueva_cota,
                cartera_nivelacion_id=cartera.id
            )

            cartera.cota = nueva_cota
            cartera.altura_instrumental = nueva_altura_instrumental
            cartera.save()

            return JsonResponse({
                "success": True,
                "message": "Punto Cambio guardado correctamente",
                "punto": punto_cambio.punto,
                "alturaInstrumental": cartera.altura_instrumental,
                "vistaMas": punto_cambio.vista_mas,
                "vistaMenos": punto_cambio.vista_menos,
                "cota": cartera.cota
            }, status=201)
            
        except CarteraNivelacion.DoesNotExist:
            return JsonResponse({
                "success": False,
                "message": "Error: No se encontró la cartera nivelación con el ID proporcionado."
            }, status=404)
        
        except Exception as e:
            print("Error:", e)  # Imprimir el error en la terminal
            print("Traceback:", traceback.format_exc())  # Ver detalles del error
            return JsonResponse({
                "success": False,
                "message": str(e) + "\n" + traceback.format_exc()
            }, status=500)
    return JsonResponse({"success": False, "message": "Método no permitido"}, status=405)

#READ CARTERA:
@login_required
def ver_cartera(request, pk):
    cartera = CarteraNivelacion.objects.get(basica_id=pk)

    basica = InformacionBasica.objects.get(pk=pk)
    return render(request, 'ver_cartera.html', {'cartera': cartera, 'basica': basica})

#UPDATE CARTERA:
@login_required
def editar_cartera_template(request, pk):
    # Asegúrate de obtener el objeto correctamente
    punto = get_object_or_404(Puntos, pk=pk)
    form = PuntosForm(instance=punto)
    return render(request, 'forms/editar_cartera.html', {'form':form, 'punto': punto})

def editar_punto(request, punto_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print(data)
            print("ID de punto recibido:", punto_id)
            tipo_punto_id = data.get("tipo_punto") or 0
            # Obtener el punto y cartera
            punto = Puntos.objects.get(id=punto_id)
            cartera = punto.cartera_nivelacion

            if (tipo_punto_id != "1"):
                punto_anterior = Puntos.objects.filter(
                    cartera_nivelacion=punto.cartera_nivelacion,  
                    id__lt=punto.id  # Filtrar solo los puntos con ID menor (anteriores)
                ).order_by("-id").first()  # Ordenar en orden descendente y tomar el primero

                cartera.altura_instrumental = punto_anterior.altura_instrumental
                cartera.cota = punto_anterior.cota

            nombre_punto = data.get("punto") or None
            if (nombre_punto == None):
                return JsonResponse({
                        "success": False,
                        "message": "Error: Debes asignar un nombre al punto."
                    }, status=400)
            

            if (tipo_punto_id == "1"):
                print("Hola desde punto BM")
                # Intentar convertir vista_mas y cota_inicial a Decimal
                try:
                    vista_mas = Decimal(data.get("vista_mas") or 0)
                except InvalidOperation:
                    return JsonResponse({
                        "success": False,
                        "message": "Error: Vista (+) no tiene un formato válido."
                    }, status=400)
                try:
                    cota_inicial = Decimal(data.get("cota") or 0)
                except InvalidOperation:
                    return JsonResponse({
                        "success": False,
                        "message": "Error: Cota no tiene un formato válido."
                    }, status=400)
                
                if (vista_mas<=0):
                    return JsonResponse({
                        "success": False,
                        "message": "Error: Vista(+) debe ser positiva."
                    }, status=400)
                
                if (cota_inicial<=0):
                    return JsonResponse({
                        "success": False,
                        "message": "Error: Cota debe ser positiva."
                    }, status=400)
                

                punto.punto=nombre_punto
                punto.vista_mas=vista_mas
                punto.cota=cota_inicial
                punto.altura_instrumental = vista_mas + cota_inicial

            elif (tipo_punto_id == "2"):
                print("Hola desde punto Delta")
                try:
                    vista_menos = Decimal(data.get("vista_menos") or 0)
                except InvalidOperation:
                    return JsonResponse({
                        "success": False,
                        "message": "Error: Vista (-) no tiene un formato válido."
                    }, status=400)

                if (vista_menos<=0):
                    return JsonResponse({
                        "success": False,
                        "message": "Error: Vista(-) debe ser positiva."
                    }, status=400)   
                
                nueva_cota = cartera.altura_instrumental - vista_menos

                if (nueva_cota<=0): 
                    return JsonResponse({
                        "success": False,
                        "message": "Error: Vista (-) no válida. La cota calculada debe ser superior a 0."
                    }, status=400)   
                
                
                punto.tipo_punto_id = tipo_punto_id
                punto.punto=nombre_punto
                punto.altura_instrumental = cartera.altura_instrumental
                punto.vista_menos= vista_menos
                punto.vista_mas = None
                punto.cota = nueva_cota

            elif (tipo_punto_id == "3"):
                print("Hola desde punto Cambio")

                try:
                    vista_mas = Decimal(data.get("vista_mas") or 0)
                except InvalidOperation:
                    return JsonResponse({
                        "success": False,
                        "message": "Error: Vista (+) no tiene un formato válido."
                    }, status=400)

                if (vista_mas<=0):
                    return JsonResponse({
                        "success": False,
                        "message": "Error: Vista(+) no puede ser negativa."
                    }, status=400)
                try:
                    vista_menos = Decimal(data.get("vista_menos") or 0)
                except InvalidOperation:
                    return JsonResponse({
                        "success": False,
                        "message": "Error: Vista (-) no tiene un formato válido."
                    }, status=400)

                if (vista_menos<=0):
                    return JsonResponse({
                        "success": False,
                        "message": "Error: Vista(-) no puede ser negativa."
                    }, status=400)
                
                nueva_cota = cartera.altura_instrumental - vista_menos

                if (nueva_cota<=0):
                    return JsonResponse({
                        "success": False,
                        "message": "Error: Vista (-) no válida. La cota calculada debe ser mayor a 0."
                    }, status=400)
                
                nueva_altura_instrumental = nueva_cota + vista_mas

                punto.tipo_punto_id = tipo_punto_id
                punto.punto=nombre_punto
                punto.altura_instrumental = nueva_altura_instrumental
                punto.vista_mas=vista_mas
                punto.vista_menos=vista_menos
                punto.cota = nueva_cota

            cartera.cota = punto.cota
            cartera.altura_instrumental = punto.altura_instrumental

            puntos_posteriores = Puntos.objects.filter(
            cartera_nivelacion=punto.cartera_nivelacion,  
            id__gt=punto.id  # Obtener solo los puntos con ID mayor (posteriores)
            ).order_by("id")  # Ordenar por ID en orden ascendente

            # Lógica para actualizar puntos posteriores
            try:
                with transaction.atomic():  # 🔹 Bloque de transacción, si algo falla se revierte todo
                    for punto_posterior in puntos_posteriores:
                        if(punto_posterior.tipo_punto_id == 2):
                            punto_posterior_nueva_cota = cartera.altura_instrumental - punto_posterior.vista_menos

                            if (punto_posterior_nueva_cota<=0):
                                raise ValueError("Error: La actualización del punto dañaría el cálculo de los puntos creados posteriormente.")

                            punto_posterior.altura_instrumental = cartera.altura_instrumental
                            punto_posterior.cota = punto_posterior_nueva_cota
                            print("Punto posterior con ID: ")
                            print(punto_posterior.id)
                            print(punto_posterior.altura_instrumental)
                            print(punto_posterior.cota)
                            
                            cartera.cota = punto_posterior.cota

                        elif(punto_posterior.tipo_punto_id == 3):
                            punto_posterior_nueva_cota = cartera.altura_instrumental - punto_posterior.vista_menos
                            if (punto_posterior_nueva_cota<=0):
                                raise ValueError("Error: La actualización del punto dañaría el cálculo de los puntos creados posteriormente.")
                            punto_posterior_nueva_altura_instrumental = punto_posterior_nueva_cota + punto_posterior.vista_mas

                            punto_posterior.altura_instrumental = punto_posterior_nueva_altura_instrumental
                            punto_posterior.cota = punto_posterior_nueva_cota

                            cartera.altura_instrumental = punto_posterior.altura_instrumental
                            cartera.cota = punto_posterior.cota

                        punto_posterior.save()

            except ValueError as e:
                return JsonResponse({"success": False, "message": str(e)}, status=400)

            except Exception as e:
                return JsonResponse({"success": False, "message": "Ocurrió un error inesperado."}, status=500)
                
            punto.save()

            cartera.save()

            return JsonResponse({
                "success": True,
                "message": "Punto actualizado correctamente",
            }, status=201)

        except InformacionBasica.DoesNotExist:
            return JsonResponse({
                "success": False,
                "message": "Error: No se encontró el punto con el ID proporcionado."
            }, status=404)

        except Exception as e:
            print("Error:", e)  # Imprimir el error en la terminal
            print("Traceback:", traceback.format_exc())  # Ver detalles del error
            return JsonResponse({
                "success": False,
                "message": f"Error inesperado: {str(e)}",
                "traceback": traceback.format_exc()
            }, status=500)

    return JsonResponse({"success": False, "message": "Método no permitido"}, status=405)

#DELETE CARTERA:
@login_required
def eliminar_punto(request, pk):
    if request.method == 'POST':  # Verifica que sea una solicitud POST

        punto = get_object_or_404(Puntos, pk=pk)  # Obtén el objeto o devuelve 404
        cartera = punto.cartera_nivelacion

        # Obtener el punto inmediatamente anterior (menor ID más cercano)
        punto_anterior = Puntos.objects.filter(
            cartera_nivelacion=punto.cartera_nivelacion,  
            id__lt=punto.id  # Filtrar solo los puntos con ID menor (anteriores)
        ).order_by("-id").first()  # Ordenar en orden descendente y tomar el primero

        puntos_posteriores = Puntos.objects.filter(
            cartera_nivelacion=punto.cartera_nivelacion,  
            id__gt=punto.id  # Obtener solo los puntos con ID mayor (posteriores)
            ).order_by("id")  # Ordenar por ID en orden ascendente

            # Lógica para actualizar puntos posteriores

        cartera.altura_instrumental = punto_anterior.altura_instrumental
        cartera.cota = punto_anterior.cota
        try:
            with transaction.atomic():  # 🔹 Bloque de transacción, si algo falla se revierte todo
                for punto_posterior in puntos_posteriores:
                    if(punto_posterior.tipo_punto_id == 2):
                        punto_posterior_nueva_cota = cartera.altura_instrumental - punto_posterior.vista_menos

                        if (punto_posterior_nueva_cota<=0):
                            raise ValueError("Error: La eliminación del punto dañaría el cálculo de los puntos creados posteriormente.")
                        punto_posterior.altura_instrumental = cartera.altura_instrumental
                        punto_posterior.cota = punto_posterior_nueva_cota
                        print("Punto posterior con ID: ")
                        print(punto_posterior.id)
                        print(punto_posterior.altura_instrumental)
                        print(punto_posterior.cota)
                            
                        cartera.cota = punto_posterior.cota

                    elif(punto_posterior.tipo_punto_id == 3):
                        punto_posterior_nueva_cota = cartera.altura_instrumental - punto_posterior.vista_menos
                        if (punto_posterior_nueva_cota<=0):
                            raise ValueError("Error: La eliminación del punto dañaría el cálculo de los puntos creados posteriormente.")
                        punto_posterior_nueva_altura_instrumental = punto_posterior_nueva_cota + punto_posterior.vista_mas
                        punto_posterior.altura_instrumental = punto_posterior_nueva_altura_instrumental
                        punto_posterior.cota = punto_posterior_nueva_cota
                        cartera.altura_instrumental = punto_posterior.altura_instrumental
                        cartera.cota = punto_posterior.cota

                    punto_posterior.save()

        except ValueError as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)

        except Exception as e:
            return JsonResponse({"success": False, "message": "Ocurrió un error inesperado."}, status=500)

        punto.delete()  # Elimina el objeto
        cartera.save()
        return JsonResponse({'success': True})  # Devuelve una respuesta JSON de éxito
    return JsonResponse({'error': 'Método no permitido'}, status=405)  # Si no es POST, responde con error

#LOGOUT:
@login_required
def logout_session(request):
    logout(request)
    return redirect('login')