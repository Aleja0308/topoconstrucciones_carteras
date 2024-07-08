from django.db import models

# Create your models here.

#Se define el modelo para los datos de la cartera:
class TipoPunto(models.Model):
  ROLES_CHOICES = (
    ('Delta', 'Delta'),
    ('Cambio', 'Cambio'),
  )

#Se define el modelo para la información básica de la cartera:
class Basica(models.Model):
  nombre = models.CharField(max_length=50)
  cuidad = models.CharField(max_length=50)
  lugar = models.CharField(max_length=50)
  responsable = models.CharField(max_length=50)
  fecha = models.DateField()

#Se define el modelo para la información numérica de la cartera:
class CarteraNivelacion(models.Model):
  basica = models.OneToOneField(Basica, on_delete= models.CASCADE, null=True)
  tipo_punto = models.ForeignKey(TipoPunto, on_delete= models.PROTECT, null=True)
  punto = models.CharField(max_length=20)
  vista_mas = models.FloatField(null=True, blank=True)
  vista_menos = models.FloatField(null=True, blank=True)
  cota = models.FloatField(null = True, blank = True)
  altura_instrumental = models.FloatField(null = True, blank = True)