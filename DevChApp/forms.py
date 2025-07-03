from django import forms
from .models import Usuario, Vehiculo, Ruta

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = '__all__'

class RutaForm(forms.ModelForm):
    class Meta:
        model = Ruta
        fields = '__all__'
