from django import forms
from .models import InformacionBasica
from .models import CarteraNivelacion
 
#Se define el formulario para Basica:
class BasicaForm(forms.ModelForm):
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
    fields = ['cota_inicial', 'vista_mas_inicial', 'tipo_punto', 'punto', 'vista_mas', 'vista_menos', 'cota_calculada']
    widgets = {
      'cota_inicial': forms.NumberInput(attrs={'type':'number','class':''}),
      'vista_mas_inicial': forms.NumberInput(attrs={'type':'number','class':''}),
      'tipo_punto': forms.Select(attrs={'class':''}),
      'punto': forms.NumberInput(attrs={'type':'number','class':''}),
      'vista_mas': forms.NumberInput(attrs={'type':'number','class':''}),
      'vista_menos': forms.NumberInput(attrs={'type':'number','class':''}),
      'cota_calculada': forms.NumberInput(attrs={'type':'number','class':''}),
}