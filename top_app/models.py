from django.db import models

# Create your models here.

#Se define el modelo para la tabla de nivelación:
class TablaNivelacion(models.Model):
  nombre = models.CharField(max_length=100)
  fecha_creacion = models.DateTimeField(auto_now_add=True)

#Se define el modelo para punto:
class Punto(models.Model):
  tabla = models.ForeignKey(TablaNivelacion, related_name='Puntos', on_delete=models.CASCADE)
  tipo = models.CharField(max_length=10, choices=[('delta', 'Delta'), ('cambio', 'Cambio')])
  vista_mas = models.FloatField(max_length=10, null = True, blank = True)
  vista_menos = models.FloatField(max_length=10, null = True, blank = True)
  cota = models.FloatField(max_length=10, null = True, blank = True)
  altura_instrumental = models.FloatField(max_length=10, null = True, blank = True)