from django import forms
from .models import Punto

#Se define el formulario para Punto:
class PuntoForm(forms.ModelForm):
  class Meta:
    model = Punto
    fields = ['tipo', 'vista_mas', 'vista_menos']