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
        fields = ['conductor', 'origen', 'destino', 'fecha', 'hora', 'cupos_disponibles']
        widgets = {
            'fecha': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
            }),
            'hora': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control',
            }),
            'origen': forms.TextInput(attrs={'class': 'form-control'}),
            'destino': forms.TextInput(attrs={'class': 'form-control'}),
            'cupos_disponibles': forms.NumberInput(attrs={'class': 'form-control'}),
            'conductor': forms.Select(attrs={'class': 'form-control'}),
        }

class RegistroForm(forms.ModelForm):
    contrasena1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    contrasena2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['nombre', 'cedula', 'correo']

    def clean_contrasena2(self):
        contrasena1 = self.cleaned_data.get("contrasena1")
        contrasena2 = self.cleaned_data.get("contrasena2")
        if contrasena1 and contrasena2 and contrasena1 != contrasena2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return contrasena2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["contrasena1"])
        if commit:
            user.save()
        return user

class VerificacionForm(forms.Form):
    codigo = forms.CharField(max_length=6)
