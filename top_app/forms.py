from django import forms
from .models import Basica
from .models import TipoPunto
from .models import CarteraNivelacion

#Se define el formulario para TipoPunto:
class TipoPuntoForm(forms.ModelForm):
  class Meta:
    model = TipoPunto
    fields = ['tipo_punto']
    widgets = {'tipo_punto': forms.Select(attrs={'class': ''})}
    
#Se define el formulario para Basica:
class BasicaForm(forms.ModelForm):
  class Meta:
    model = Basica
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
    fields = ['punto', 'vista_mas', 'vista_menos', 'cota']
    widgets = {
      'punto': forms.NumberInput(attrs={'type':'number','class':''}),
      'vista_mas': forms.NumberInput(attrs={'type':'number','class':''}),
      'vista_menos': forms.NumberInput(attrs={'type':'number','class':''}),
      'cota': forms.NumberInput(attrs={'type':'number','class':''}),
      }
  