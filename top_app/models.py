from django.db import models

# Modelo para la información básica de la cartera
class InformacionBasica(models.Model):
    nombre = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=50)
    lugar = models.CharField(max_length=50)
    responsable = models.CharField(max_length=50)
    fecha = models.DateField()
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

# Modelo para la información numérica de la cartera
class CarteraNivelacion(models.Model):
    ROLES_CHOICES = (
        ('BM', 'BM'),
        ('Delta', 'Delta'),
        ('Cambio', 'Cambio'),
    )
    tipo_punto = models.CharField(max_length=20, choices=ROLES_CHOICES)
    punto = models.CharField(max_length=20)
    altura_instrumental = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    vista_mas = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    vista_menos = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    cota = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    basica = models.ForeignKey(InformacionBasica, on_delete=models.CASCADE, related_name='carteras', default=1)

    def __str__(self):
        return f'{self.tipo_punto} - {self.punto}'

    