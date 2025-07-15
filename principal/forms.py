from django import forms
from .models import Usuario
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class RegistroForm(forms.ModelForm):
    confirmar_contraseña = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Usuario
        fields = ['nombre', 'correo', 'numero', 'contraseña']
        widgets = {'contraseña': forms.PasswordInput()}

    def clean_confirmar_contraseña(self):
        contraseña = self.cleaned_data.get("contraseña")
        confirmar = self.cleaned_data.get("confirmar_contraseña")
        if contraseña and confirmar and contraseña != confirmar:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return confirmar

class LoginForm(forms.Form):
    correo_o_numero = forms.CharField()
    contraseña = forms.CharField(widget=forms.PasswordInput())

class RecuperarForm(forms.Form):
    correo = forms.EmailField()


