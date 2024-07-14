from django.db import models

# Create your models here.

#Se define el modelo para la información básica de la cartera:
class InformacionBasica(models.Model):
  nombre = models.CharField(max_length=50)
  ciudad = models.CharField(max_length=50)
  lugar = models.CharField(max_length=50)
  responsable = models.CharField(max_length=50)
  fecha = models.DateField()

#Se define el modelo para la información numérica de la cartera:
class CarteraNivelacion(models.Model):
  ROLES_CHOICES = (
    ('delta', 'Delta'),
    ('cambio', 'Cambio'),
  )
  bench_mark = models.FloatField(null = True, blank = True)
  cota_inicial = models.FloatField(null = True, blank = True)
  vista_mas_inicial = models.FloatField(null=True, blank=True)
  tipo_punto = models.CharField(max_length=20, choices=ROLES_CHOICES)
  punto = models.CharField(max_length=20)
  vista_mas = models.FloatField(null=True, blank=True)
  vista_menos = models.FloatField(null=True, blank=True)
  cota_calculada = models.FloatField(null=True, blank=True)
  altura_instrumental = models.FloatField(null = True, blank = True)
  basica = models.OneToOneField(InformacionBasica, on_delete= models.CASCADE, null=True)

  def __str__(self):
    return self.tipo_punto