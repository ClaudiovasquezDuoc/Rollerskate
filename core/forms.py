from django import forms
from .models import Producto
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# --------------------------
# FORMULARIO: EDICIÓN DE PERFIL
# --------------------------
class EditarUsuarioForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Nueva Contraseña',
        widget=forms.PasswordInput,
        required=False,
        help_text="Dejar en blanco si no deseas cambiarla.",
    )
    password2 = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput,
        required=False,
    )

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                raise ValidationError("Las contraseñas no coinciden.")
            validate_password(password1)

        return cleaned_data
    
