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
    cota_inicial = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    cota_calculada = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    basica = models.OneToOneField(InformacionBasica, on_delete = models.CASCADE, null=True)

    def __str__(self):
        return self.tipo_punto

    # Lógica para calcular la cota en función del tipo de punto
    def calcular_cota(self):
        if self.tipo_punto == 'BM':
            # Si es BM, se calcula altura instrumental como cota inicial + vista más:
            if self.cota_inicial is not None and self.vista_mas is not None:
                self.altura_instrumental = self.cota_inicial + self.vista_mas

        elif self.tipo_punto == 'Delta':
            # Si es Delta, se calcula la cota calculada como altura instrumental - vista menos:
            if self.altura_instrumental is not None and self.vista_menos is not None:
                self.cota_calculada = self.altura_instrumental - self.vista_menos

        elif self.tipo_punto == 'Cambio':
            # Si es Cambio, se realizan ambos cálculos:
            if self.altura_instrumental is not None and self.vista_menos is not None:
                self.cota_calculada = self.altura_instrumental - self.vista_menos
            if self.cota_calculada is not None and self.vista_mas is not None:
                self.altura_instrumental = self.cota_calculada + self.vista_mas

        # Guarda los cambios en la instancia
        self.save()