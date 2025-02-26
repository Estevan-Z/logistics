from django import forms
from .models import Proveedor, ParametrosProducto, Producto

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = [
            'nombre_comercial',
            'representante_legal',
            'nit',
            'direccion',
            'telefono',
            'correo_electronico',
        ]
        widgets = {
            'nombre_comercial': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre Comercial'}),
            'representante_legal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Representante Legal'}),
            'nit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'NIT'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'correo_electronico': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo Electrónico'}),
        }


class ProductoForm(forms.ModelForm):
    grupo = forms.ChoiceField(choices=[], required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    linea = forms.ChoiceField(choices=[], required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    unidad = forms.ChoiceField(choices=[], required=True, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Producto
        fields = ['nombre_producto', 'marca', 'grupo', 'linea', 'unidad']
        widgets = {
            'nombre_producto': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        opcion_predeterminada = [('','-------------')]
        
        self.fields['grupo'].choices = opcion_predeterminada + [
            (param.grupo, param.grupo) for param in ParametrosProducto.objects.exclude(grupo__isnull=True).distinct()
        ]
        self.fields['linea'].choices = opcion_predeterminada + [
            (param.linea, param.linea) for param in ParametrosProducto.objects.exclude(linea__isnull=True).distinct()
        ]
        self.fields['unidad'].choices = opcion_predeterminada + [
            (param.unidad, param.unidad) for param in ParametrosProducto.objects.exclude(unidad__isnull=True).distinct()
        ]
