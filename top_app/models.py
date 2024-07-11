from django.db import models

# Create your models here.

#Se define el modelo para TipoPunto:
class TipoPunto(models.Model):
  ROLES_CHOICES = (
    ('BM', 'BM'),
    ('delta', 'Delta'),
    ('cambio', 'Cambio'),
  )
  tipo_punto = models.CharField(max_length=20, choices=ROLES_CHOICES)
  
  def __str__(self):
    return self.tipo_punto

#Se define el modelo para la información básica de la cartera:
class InformacionBasica(models.Model):
  nombre = models.CharField(max_length=50)
  ciudad = models.CharField(max_length=50)
  lugar = models.CharField(max_length=50)
  responsable = models.CharField(max_length=50)
  fecha = models.DateField()

#Se define el modelo para la información numérica de la cartera:
class CarteraNivelacion(models.Model):
  basica = models.OneToOneField(InformacionBasica, on_delete= models.CASCADE, null=True)
  tipo_punto = models.ForeignKey(TipoPunto, on_delete= models.PROTECT, null=True)
  punto = models.CharField(max_length=20)
  vista_mas = models.FloatField(null=True, blank=True)
  vista_menos = models.FloatField(null=True, blank=True)
  cota = models.FloatField(null = True, blank = True)
  altura_instrumental = models.FloatField(null = True, blank = True)
