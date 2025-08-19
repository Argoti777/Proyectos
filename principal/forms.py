from django import forms
from .models import *
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin



class crearLigaForm(forms.ModelForm):
    class Meta:
        model = Liga
        fields = ['nombre', 'pais', 'ciudad', 'fecha_inicio', 'fecha_fin']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
        }

class crearEquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = ['nombre', 'ciudad', 'liga', 'logo']

class crearJugadorForm(forms.ModelForm):
    class Meta:
        model = Jugador
        fields = ['nombre', 'apellido', 'edad', 'posicion', 'equipo', 'foto']
        



class LoginForm(forms.Form):
    correo_o_numero = forms.CharField()
    contraseña = forms.CharField(widget=forms.PasswordInput())

class RecuperarForm(forms.Form):
    correo = forms.EmailField()



