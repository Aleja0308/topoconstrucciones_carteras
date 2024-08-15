from django import forms
from .models import InformacionBasica, CarteraNivelacion

class InformacionBasicaForm(forms.ModelForm):
    class Meta:
        model = InformacionBasica
        fields = ['nombre', 'ciudad', 'lugar', 'responsable', 'fecha', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'lugar': forms.TextInput(attrs={'class': 'form-control'}),
            'responsable': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
        }

class CarteraNivelacionForm(forms.ModelForm):
    class Meta:
        model = CarteraNivelacion
        fields = ['tipo_punto', 'punto', 'altura_instrumental', 'vista_mas', 'vista_menos', 'cota_inicial', 'cota_calculada', 'basica']
        widgets = {
            'tipo_punto': forms.Select(attrs={'class': 'form-control'}),
            'punto': forms.TextInput(attrs={'class': 'form-control'}),
            'altura_instrumental': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'vista_mas': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'vista_menos': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'cota_inicial': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'cota_calculada': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'basica': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        tipo_punto = cleaned_data.get('tipo_punto')
        cota_inicial = cleaned_data.get('cota_inicial')
        vista_mas = cleaned_data.get('vista_mas')
        vista_menos = cleaned_data.get('vista_menos')

        if tipo_punto == 'BM' and cota_inicial is None:
            self.add_error('cota_inicial', 'Para el tipo de punto BM, la cota inicial es obligatoria.')
        elif tipo_punto == 'Delta' and vista_menos is None:
            self.add_error('vista_menos', 'Para el tipo de punto Delta, la vista (-) es obligatoria.')
        elif tipo_punto == 'Cambio':
            if vista_mas is None:
                self.add_error('vista_mas', 'Para el tipo de punto Cambio, la vista (+) es obligatoria.')
            if vista_menos is None:
                self.add_error('vista_menos', 'Para el tipo de punto Cambio, la vista (-) también es obligatoria.')
        return cleaned_data