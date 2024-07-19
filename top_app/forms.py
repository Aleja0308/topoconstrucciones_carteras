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

  def clean(self):
      cleaned_data = super().clean()
      tipo_punto = cleaned_data.get('tipo_punto')
      cota_inicial = cleaned_data.get('cota_inicial')
      vista_mas = cleaned_data.get('vista_mas')
      vista_menos = cleaned_data.get('vista_menos')
      
      if tipo_punto == 'BM' and cota_inicial is None:
          self.add_error('cota_inicial', 'La Cota del BM es requerida para tipo de punto BM.')
      elif tipo_punto == 'Delta' and vista_menos in None:
          self.add_error('vista_menos' 'Vista (-) es requerida para tipo de punto Delta.')
      elif tipo_punto == 'Cambio' and vista_mas in None:
          self.add_error('vista_mas' 'Vista (+) es requerida para tipo de punto Cambio.')
      return cleaned_data

  def save(self, commit=True):
      instance = super().save(commit=False)
      if instance.cota_inicial is None:
          instance.cota_inicial = 0  # Valor inicial predeterminado, ajustar según sea necesario
      instance.altura_instrumental = instance.vista_mas + instance.cota_inicial if instance.vista_mas else instance.altura_instrumental
      instance.calcular_cota()
      if commit:
          instance.save()
      return instance