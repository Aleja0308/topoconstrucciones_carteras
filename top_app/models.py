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
    ('BM', 'BM'),
    ('Delta', 'Delta'),
    ('Cambio', 'Cambio'),
  )
  tipo_punto = models.CharField(max_length=20, choices=ROLES_CHOICES)
  punto = models.CharField(max_length=20)
  altura_instrumental = models.FloatField(blank = True)
  vista_mas = models.FloatField(blank=True)
  vista_menos = models.FloatField(blank=True)
  cota_inicial = models.FloatField(blank = True)
  cota_calculada = models.FloatField(blank=True)
  basica = models.OneToOneField(InformacionBasica, on_delete= models.CASCADE, null=True)

  def __str__(self):
    return self.tipo_punto
  
  def calcular_cota(self):
      if self.tipo_punto == 'BM':
          self.altura_instrumental = self.cota_inicial + self.vista_mas
      elif self.tipo_punto == 'Delta':
          self.cota_calculada = self.altura_instrumental - self.vista_menos
      elif self.tipo_punto == 'Cambio':
          self.cota_calculada = self.altura_instrumental - self.vista_menos
          self.altura_instrumental = self.cota_calculada + self.vista_mas
      self.save()