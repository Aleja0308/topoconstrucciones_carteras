from django import forms
from .models import InformacionBasica, CarteraNivelacion, TipoPunto, Puntos
from decimal import Decimal

class InformacionBasicaForm(forms.ModelForm):
    class Meta:
        model = InformacionBasica
        fields = ['nombre', 'ciudad', 'lugar', 'responsable', 'fecha', 'descripcion']
        widgets = {
            field: forms.TextInput(attrs={
                'class': 'block py-2.5 px-0 w-full text-sm text-black bg-transparent border-0 border-b-2 border-gray-700 appearance-none dark:text-white dark:border-gray-500 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer',
                'placeholder': ' ',
                'required': True,
                'id': field
            }) for field in ['nombre', 'ciudad', 'lugar', 'responsable']
        }
        widgets['fecha'] = forms.DateInput(attrs={
            'class': widgets['nombre'].attrs['class'],
            'placeholder': ' ',
            'required': True,
            'id': 'fecha'
        })
        widgets['descripcion'] = forms.Textarea(attrs={
            'class': widgets['nombre'].attrs['class'],
            'placeholder': ' ',
            'required': True,
            'id': 'descripcion',
            'rows': 5,
            'cols': 50
        })

class PuntosForm(forms.ModelForm):
    class Meta:
        model = Puntos
        fields = ['tipo_punto', 'punto', 'altura_instrumental', 'vista_mas', 'vista_menos']
        widgets = {
            'tipo_punto': forms.Select(attrs={'class': 'w-full p-2 rounded-md border'}),
            'punto': forms.TextInput(attrs={'class': 'w-full p-2 rounded-md border'}),
            'altura_instrumental': forms.NumberInput(attrs={'class': 'w-full p-2 rounded-md border', 'step': 'any'}),
            'vista_mas': forms.NumberInput(attrs={'class': 'w-full p-2 rounded-md border', 'step': 'any'}),
            'vista_menos': forms.NumberInput(attrs={'class': 'w-full p-2 rounded-md border', 'step': 'any'}),
        }

class CarteraNivelacionForm(forms.ModelForm):
    tipo_punto = forms.ModelChoiceField(
        queryset=TipoPunto.objects.all(),
        widget=forms.Select(attrs={'class': 'w-full p-2 rounded-md border'})
    )
    punto = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'w-full p-2 rounded-md border'})
    )
    altura_instrumental = forms.DecimalField(
        required=False, widget=forms.NumberInput(attrs={'class': 'w-full p-2 rounded-md border', 'step': 'any'})
    )
    cota = forms.DecimalField(
        required=False, widget=forms.NumberInput(attrs={'class': 'w-full p-2 rounded-md border', 'step': 'any'})
    )
    vista_mas = forms.DecimalField(
        required=False, widget=forms.NumberInput(attrs={'class': 'w-full p-2 rounded-md border', 'step': 'any'})
    )
    vista_menos = forms.DecimalField(
        required=False, widget=forms.NumberInput(attrs={'class': 'w-full p-2 rounded-md border', 'step': 'any'})
    )

    class Meta:
        model = CarteraNivelacion
        fields = ['altura_instrumental', 'cota']

    def clean(self):
        cleaned_data = super().clean()
        tipo_punto = cleaned_data.get('tipo_punto')
        altura_instrumental = cleaned_data.get('altura_instrumental')
        vista_mas = cleaned_data.get('vista_mas')
        vista_menos = cleaned_data.get('vista_menos')
        cota = cleaned_data.get('cota')

        if altura_instrumental is not None:
            altura_instrumental = Decimal(altura_instrumental)
        if vista_mas is not None:
            vista_mas = Decimal(vista_mas)
        if vista_menos is not None:
            vista_menos = Decimal(vista_menos)
        if cota is not None:
            cota = Decimal(cota)

        if tipo_punto and tipo_punto.nombre == "BM":
            if cota is None:
                self.add_error('cota', 'Para el tipo de punto BM, la cota inicial es obligatoria.')
            if altura_instrumental is None and cota is not None and vista_mas is not None:
                cleaned_data['altura_instrumental'] = cota + vista_mas
        elif tipo_punto and tipo_punto.nombre == "Delta":
            if vista_menos is None:
                self.add_error('vista_menos', 'Para el tipo de punto Delta, la vista (-) es obligatoria.')
            if cota is None and altura_instrumental is not None and vista_menos is not None:
                cleaned_data['cota'] = altura_instrumental - vista_menos
        elif tipo_punto and tipo_punto.nombre == "Cambio":
            if vista_mas is None:
                self.add_error('vista_mas', 'Para el tipo de punto Cambio, la vista (+) es obligatoria.')
            if vista_menos is None:
                self.add_error('vista_menos', 'Para el tipo de punto Cambio, la vista (-) también es obligatoria.')
            if altura_instrumental is None and cota is not None and vista_mas is not None:
                cleaned_data['altura_instrumental'] = cota + vista_mas
            if cota is None and altura_instrumental is not None and vista_menos is not None:
                cleaned_data['cota'] = altura_instrumental - vista_menos
        
        return cleaned_data

    def save(self, commit=True):
        cartera = super().save(commit=False)
        if commit:
            cartera.save()
        
        Puntos.objects.create(
            tipo_punto=self.cleaned_data['tipo_punto'],
            punto=self.cleaned_data['punto'],
            cartera_nivelacion=cartera,
            altura_instrumental=self.cleaned_data.get('altura_instrumental'),
            vista_mas=self.cleaned_data.get('vista_mas'),
            vista_menos=self.cleaned_data.get('vista_menos'),
            cota=self.cleaned_data.get('cota')
        )
        
        return cartera
