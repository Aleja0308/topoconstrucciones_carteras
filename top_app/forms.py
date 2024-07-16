from django import forms
from .models import InformacionBasica
from .models import CarteraNivelacion
 
#Se define el formulario para Basica:
class InformacionBasicaForm(forms.ModelForm):
  class Meta:
    model = InformacionBasica
    fields = ['nombre', 'ciudad', 'lugar', 'responsable', 'fecha']
    widgets = {
      'nombre': forms.TextInput(attrs={'type': 'text', 'class':''}),
      'ciudad': forms.TextInput(attrs={'type': 'text', 'class':''}),
      'lugar': forms.TextInput(attrs={'type': 'text', 'class':''}),
      'responsable': forms.TextInput(attrs={'type': 'text', 'class':''}),
      'fecha': forms.DateInput(attrs={'type': 'date', 'class':''}),
    }

#Se define el formulario para CarteraNivelacion:
class CarteraNivelacionForm(forms.ModelForm):
  class Meta:
    model = CarteraNivelacion
    fields = ['tipo_punto', 'punto', 'vista_mas', 'vista_menos', 'cota_inicial', 'cota_calculada']
    widgets = {
      'tipo_punto': forms.Select(attrs={'class':''}),
      'punto': forms.NumberInput(attrs={'type':'number','class':''}),
      'vista_mas': forms.NumberInput(attrs={'type':'number','class':''}),
      'vista_menos': forms.NumberInput(attrs={'type':'number','class':''}),
      'cota_inicial': forms.NumberInput(attrs={'type':'number','class':''}),
      'cota_calculada': forms.NumberInput(attrs={'type':'number','class':''}),
}