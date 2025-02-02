from django import forms
from .models import InformacionBasica, CarteraNivelacion, TipoPunto, Punto, PuntoBM, PuntoDelta, PuntoCambio
from decimal import Decimal

class InformacionBasicaForm(forms.ModelForm):
    class Meta:
        model = InformacionBasica
        fields = ['nombre', 'ciudad', 'lugar', 'responsable', 'fecha', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'block py-2.5 px-0 w-full text-sm text-black bg-transparent border-0 border-b-2 border-gray-700 appearance-none dark:text-white dark:border-gray-500 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer',
                'placeholder': ' ',
                'required': True,
                'id': 'nombre'
            }),
            'ciudad': forms.TextInput(attrs={
                'class': 'block py-2.5 px-0 w-full text-sm text-black bg-transparent border-0 border-b-2 border-gray-700 appearance-none dark:text-white dark:border-gray-500 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer',
                'placeholder': ' ',
                'required': True,
                'id': 'ciudad'
            }),
            'lugar': forms.TextInput(attrs={
                'class': 'block py-2.5 px-0 w-full text-sm text-black bg-transparent border-0 border-b-2 border-gray-700 appearance-none dark:text-white dark:border-gray-500 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer',
                'placeholder': ' ',
                'required': True,
                'id': 'lugar'
            }),
            'responsable': forms.TextInput(attrs={
                'class': 'block py-2.5 px-0 w-full text-sm text-black bg-transparent border-0 border-b-2 border-gray-700 appearance-none dark:text-white dark:border-gray-500 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer',
                'placeholder': ' ',
                'required': True,
                'id': 'responsable'
            }),
            'fecha': forms.DateInput(attrs={
                'class': 'block py-2.5 px-0 w-full text-sm text-black bg-transparent border-0 border-b-2 border-gray-700 appearance-none dark:text-white dark:border-gray-500 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer',
                'placeholder': ' ',
                'required': True,
                'id': 'fecha'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'block py-2.5 px-0 w-full text-sm text-black bg-transparent border-0 border-b-2 border-gray-700 appearance-none dark:text-white dark:border-gray-500 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer',
                'placeholder': ' ',
                'required': True,
                'id': 'descripcion',
                'rows': 5,
                'cols': 50
            }),
        }

class PuntoForm(forms.ModelForm):
    class Meta:
        model = Punto
        fields = ['tipo_punto', 'punto']
        widgets = {
            'tipo_punto': forms.Select(attrs={'class': 'w-full p-2 rounded-md border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:focus:ring-indigo-400 dark:focus:border-indigo-400'}),
            'punto': forms.TextInput(attrs={'class': 'w-full p-2 rounded-md border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:focus:ring-indigo-400 dark:focus:border-indigo-400'}),
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
    vista_mas = forms.DecimalField(
        required=False, widget=forms.NumberInput(attrs={'class': 'w-full p-2 rounded-md border', 'step': 'any'})
    )
    vista_menos = forms.DecimalField(
        required=False, widget=forms.NumberInput(attrs={'class': 'w-full p-2 rounded-md border', 'step': 'any'})
    )
    cota = forms.DecimalField(
        required=False, widget=forms.NumberInput(attrs={'class': 'w-full p-2 rounded-md border', 'step': 'any'})
    )

    class Meta:
        model = CarteraNivelacion
        fields = ['altura_instrumental']

    def clean(self):
        cleaned_data = super().clean()
        tipo_punto = int(cleaned_data.get('tipo_punto'))
        altura_instrumental = cleaned_data.get('altura_instrumental')
        vista_mas = cleaned_data.get('vista_mas')
        vista_menos = cleaned_data.get('vista_menos')
        cota = cleaned_data.get('cota')

        # Convierte los valores a Decimal si no son None
        if altura_instrumental is not None:
            altura_instrumental = Decimal(altura_instrumental)
        if vista_mas is not None:
            vista_mas = Decimal(vista_mas)
        if vista_menos is not None:
            vista_menos = Decimal(vista_menos)
        if cota is not None:
            cota = Decimal(cota)

        # Validaciones y cálculos según el tipo de punto
        if tipo_punto == 1:  # BM
            if cota is None:
                self.add_error('cota', 'Para el tipo de punto BM, la cota inicial es obligatoria.')
            if altura_instrumental is None and cota is not None and vista_mas is not None:
                cleaned_data['altura_instrumental'] = cota + vista_mas

        elif tipo_punto == 2:  # Delta
            if vista_menos is None:
                self.add_error('vista_menos', 'Para el tipo de punto Delta, la vista (-) es obligatoria.')
            if cota is None and altura_instrumental is not None and vista_menos is not None:
                cleaned_data['cota'] = altura_instrumental - vista_menos

        elif tipo_punto == 3:  # Cambio
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
        cartera.save()

        tipo_punto = int(self.cleaned_data['tipo_punto'])
        punto = self.cleaned_data['punto']
        altura_instrumental = self.cleaned_data.get('altura_instrumental')
        vista_mas = self.cleaned_data.get('vista_mas')
        vista_menos = self.cleaned_data.get('vista_menos')
        cota = self.cleaned_data.get('cota')

        if tipo_punto == 1:  # BM
            bm = PuntoBM.objects.create(vista_mas=vista_mas, cota_inicial=cota)
            Punto.objects.create(tipo_punto=tipo_punto, punto=punto, cartera_nivelacion=cartera, registro_id=bm.id)

        elif tipo_punto == 2:  # Delta
            delta = PuntoDelta.objects.create(vista_menos=vista_menos)
            Punto.objects.create(tipo_punto=tipo_punto, punto=punto, cartera_nivelacion=cartera, registro_id=delta.id)

        elif tipo_punto == 3:  # Cambio
            cambio = PuntoCambio.objects.create(vista_mas=vista_mas, vista_menos=vista_menos)
            Punto.objects.create(tipo_punto=tipo_punto, punto=punto, cartera_nivelacion=cartera, registro_id=cambio.id)

        return cartera