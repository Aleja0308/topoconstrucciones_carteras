from django.db import models

# Se define el modelo para la información básica de la cartera:
from django.db import models

# Modelo para la información básica de la cartera
class InformacionBasica(models.Model):
    nombre = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=50)
    lugar = models.CharField(max_length=50)
    responsable = models.CharField(max_length=50)
    fecha = models.DateField()
    descripcion = models.CharField(max_length=100)

# Modelo para la información numérica de la cartera
class CarteraNivelacion(models.Model):
    ROLES_CHOICES = (
        ('BM', 'BM'),
        ('Delta', 'Delta'),
        ('Cambio', 'Cambio'),
    )
    tipo_punto = models.CharField(max_length=20, choices=ROLES_CHOICES)
    punto = models.CharField(max_length=20)
    altura_instrumental = models.FloatField(blank=True, null=True)
    vista_mas = models.FloatField(blank=True, null=True)
    vista_menos = models.FloatField(blank=True, null=True)
    cota_inicial = models.FloatField(blank=True, null=True)
    cota_calculada = models.FloatField(blank=True, null=True)
    basica = models.OneToOneField(InformacionBasica, on_delete=models.CASCADE, null= True)

    def __str__(self):
        return self.tipo_punto

    def calcular_cota(self):
        # Lógica para calcular la cota en función del tipo de punto
        if self.tipo_punto == 'BM':
            if self.cota_inicial is not None and self.vista_mas is not None:
                self.altura_instrumental = self.cota_inicial + self.vista_mas
        elif self.tipo_punto == 'Delta':
            if self.altura_instrumental is not None and self.vista_menos is not None:
                self.cota_calculada = self.altura_instrumental - self.vista_menos
        elif self.tipo_punto == 'Cambio':
            if self.altura_instrumental is not None and self.vista_menos is not None:
                self.cota_calculada = self.altura_instrumental - self.vista_menos
            if self.cota_calculada is not None and self.vista_mas is not None:
                self.altura_instrumental = self.cota_calculada + self.vista_mas
        self.save()