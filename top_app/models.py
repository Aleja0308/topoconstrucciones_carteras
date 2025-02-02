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

# Modelo base para la información numérica de la cartera
class CarteraNivelacion(models.Model):
    basica = models.ForeignKey(InformacionBasica, on_delete=models.CASCADE)
    altura_instrumental = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    cota = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Cartera de {self.basica.nombre}'

class TipoPunto(models.Model):
    nombre = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.nombre
    
# Modelo que conecta CarteraNivelacion con los puntos específicos
class Punto(models.Model):

    tipo_punto = models.ForeignKey(TipoPunto, on_delete=models.CASCADE)
    punto = models.CharField(max_length=20)  # Descripción del punto
    cartera_nivelacion = models.ForeignKey(CarteraNivelacion, on_delete=models.CASCADE)
    registro_id = models.PositiveIntegerField()  # ID del punto específico (BM, Delta o Cambio)

    def __str__(self):
        return f'{self.tipo_punto.nombre} - {self.punto} ({self.cartera_nivelacion.basica.nombre})'

# Modelo para puntos BM (Solo uno por CarteraNivelacion)
class PuntoBM(models.Model):
    vista_mas = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    cota_inicial = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)

    def __str__(self):
        return f'BM - {self.id}'

# Modelo para puntos Delta (Múltiples por CarteraNivelacion)
class PuntoDelta(models.Model):
    vista_menos = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Delta - {self.id}'

# Modelo para puntos Cambio (Múltiples por CarteraNivelacion)
class PuntoCambio(models.Model):
    vista_mas = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    vista_menos = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Cambio - {self.id}'
