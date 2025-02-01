from django import forms
from .models import InformacionBasica, CarteraNivelacion
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

class CarteraNivelacionForm(forms.ModelForm):
    class Meta:
        model = CarteraNivelacion
        fields = ['tipo_punto', 'punto', 'altura_instrumental', 'vista_mas', 'vista_menos', 'cota']
        widgets = {
            'tipo_punto': forms.Select(attrs={'class': 'w-full p-2 rounded-md border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:focus:ring-indigo-400 dark:focus:border-indigo-400'}),
            'punto': forms.TextInput(attrs={'class': 'w-full p-2 rounded-md border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:focus:ring-indigo-400 dark:focus:border-indigo-400'}),
            'altura_instrumental': forms.NumberInput(attrs={'class': 'w-full p-2 rounded-md border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:focus:ring-indigo-400 dark:focus:border-indigo-400', 'step': 'any'}),
            'vista_mas': forms.NumberInput(attrs={'class': 'w-full p-2 rounded-md border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:focus:ring-indigo-400 dark:focus:border-indigo-400', 'step': 'any'}),
            'vista_menos': forms.NumberInput(attrs={'class': 'w-full p-2 rounded-md border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:focus:ring-indigo-400 dark:focus:border-indigo-400', 'step': 'any'}),
            'cota': forms.NumberInput(attrs={'class': 'w-full p-2 rounded-md border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:focus:ring-indigo-400 dark:focus:border-indigo-400', 'step': 'any'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        tipo_punto = cleaned_data.get('tipo_punto')
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

        # Validaciones y cálculos
        if tipo_punto == 'BM':
            if cota is None:
                self.add_error('cota', 'Para el tipo de punto BM, la cota inicial es obligatoria.')
            if altura_instrumental is None and cota is not None and vista_mas is not None:
                cleaned_data['altura_instrumental'] = cota + vista_mas

        elif tipo_punto == 'Delta':
            if vista_menos is None:
                self.add_error('vista_menos', 'Para el tipo de punto Delta, la vista (-) es obligatoria.')
            if cota is None and altura_instrumental is not None and vista_menos is not None:
                cleaned_data['cota'] = altura_instrumental - vista_menos

        elif tipo_punto == 'Cambio':
            if vista_mas is None:
                self.add_error('vista_mas', 'Para el tipo de punto Cambio, la vista (+) es obligatoria.')
            if vista_menos is None:
                self.add_error('vista_menos', 'Para el tipo de punto Cambio, la vista (-) también es obligatoria.')
            if altura_instrumental is None and cota is not None and vista_mas is not None:
                cleaned_data['altura_instrumental'] = cota + vista_mas
            if cota is None and altura_instrumental is not None and vista_menos is not None:
                cleaned_data['cota'] = altura_instrumental - vista_menos

        return cleaned_data