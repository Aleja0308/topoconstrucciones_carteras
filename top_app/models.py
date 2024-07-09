from django.db import models

# Create your models here.

#Se define el modelo para :
class TipoPunto(models.Model):
  ROLES_CHOICES = (
    ('Delta', 'Delta'),
    ('Cambio', 'Cambio'),
  )
  tipo_punto = models.CharField(max_length=20, choices=ROLES_CHOICES)
  
  def __str__(self):
    return self.tipo_punto

#Se define el modelo para la información básica de la cartera:
class Basica(models.Model):
  nombre = models.CharField(max_length=50)
  ciudad = models.CharField(max_length=50)
  lugar = models.CharField(max_length=50)
  responsable = models.CharField(max_length=50)
  fecha = models.DateField()
  
  def __str__(self):
    return self.nombre

#Se define el modelo para la información numérica de la cartera:
class CarteraNivelacion(models.Model):
  basica = models.OneToOneField(Basica, on_delete= models.CASCADE, null=True)
  tipo_punto = models.ForeignKey(TipoPunto, on_delete= models.PROTECT, null=True)
  punto = models.CharField(max_length=20)
  vista_mas = models.FloatField(null=True, blank=True)
  vista_menos = models.FloatField(null=True, blank=True)
  cota = models.FloatField(null = True, blank = True)
  altura_instrumental = models.FloatField(null = True, blank = True)
  
  def save(self, *args, **kwargs):
      if self.vista_mas is not None and self.vista_menos is not None:
          self.cota = self.vista_mas - self.vista_menos
          self.altura_instrumental = self.cota + self.vista_mas
      super().save(*args, **kwargs)

  def __str__(self):
      return f"Punto {self.nombre_punto} de {self.cartera.nombre}"