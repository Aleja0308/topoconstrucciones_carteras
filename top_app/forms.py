from django import forms
from django.forms import inlineformset_factory
from .models import InformacionBasica
from .models import CarteraNivelacion

# Se define el formulario para Basica:
class InformacionBasicaForm(forms.ModelForm):
    class Meta:
        model = InformacionBasica
        fields = ['nombre', 'ciudad', 'lugar', 'responsable', 'fecha', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'type': 'text', 'class': ''}),
            'ciudad': forms.TextInput(attrs={'type': 'text', 'class': ''}),
            'lugar': forms.TextInput(attrs={'type': 'text', 'class': ''}),
            'responsable': forms.TextInput(attrs={'type': 'text', 'class': ''}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': ''}),
            'descripcion': forms.Textarea(attrs={'type': 'date', 'class': ''}),
        }

# Se define el formulario para CarteraNivelacion:
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
        elif tipo_punto == 'Delta' and vista_menos is None:
            self.add_error('vista_menos', 'Vista (-) es requerida para tipo de punto Delta.')
        elif tipo_punto == 'Cambio' and vista_mas is None:
            self.add_error('vista_mas', 'Vista (+) es requerida para tipo de punto Cambio.')
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Asignar valores predeterminados si alguno de los valores es None
        if instance.cota_inicial is None:
            instance.cota_inicial = 0.0
        if instance.vista_mas is None:
            instance.vista_mas = 0.0
        if instance.vista_menos is None:
            instance.vista_menos = 0.0

        # Calcular altura instrumental solo si vista_mas no es None
        if instance.vista_mas is not None:
            instance.altura_instrumental = instance.vista_mas + instance.cota_inicial
        else:
            instance.altura_instrumental = None

        # Asegurarse de que calcular_cota existe y llamarlo
        if hasattr(instance, 'calcular_cota') and callable(getattr(instance, 'calcular_cota')):
            instance.calcular_cota()

        if commit:
            instance.save()
        return instance

# Crear el formset para CarteraNivelacion:
CarteraNivelacionFormSet = inlineformset_factory(
    InformacionBasica,
    CarteraNivelacion,
    form=CarteraNivelacionForm,
    extra=1,
    can_delete=True
)