from django import forms
from .models import *
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin



from django import forms
from django.utils import timezone
from datetime import timedelta
from .models import Liga

class crearLigaForm(forms.ModelForm):

    class Meta:
        model = Liga
        fields = ['nombre', 'pais', 'ciudad', 'descripcion', 'fecha_inicio', 'fecha_fin']
        widgets = {'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'id': 'fecha_inicio'}),
                   'fecha_fin': forms.DateInput(attrs={'type': 'date', 'id': 'fecha_fin'}),}

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')

        hoy = timezone.now().date()
        manana = hoy + timedelta(days=1)

        # 1️⃣ La liga debe iniciar desde mañana
        if fecha_inicio and fecha_inicio < manana:
            raise forms.ValidationError(
                "La liga debe iniciar como mínimo desde el día de mañana."
            )

        # 2️⃣ Duración mínima de 1 mes
        if fecha_inicio and fecha_fin:
            duracion_minima = fecha_inicio + timedelta(days=30)
            if fecha_fin < duracion_minima:
                raise forms.ValidationError(
                    "La liga debe tener una duración mínima de 1 mes."
                )

        return cleaned_data


class crearEquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = ['nombre', 'ciudad', 'liga', 'logo']
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # recibimos el usuario desde la vista
        super().__init__(*args, **kwargs)
        if user:
            # solo ligas del administrador
            self.fields['liga'].queryset = Liga.objects.filter(administrador=user)

class crearJugadorForm(forms.ModelForm):
    class Meta:
        model = Jugador
        fields = ['cedula', 'nombre', 'apellido', 'edad', 'posicion', 'equipo', 'foto']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['equipo'].queryset = Equipo.objects.filter(liga__administrador=user)

class LoginForm(forms.Form):
    correo_o_numero = forms.CharField()
    contraseña = forms.CharField(widget=forms.PasswordInput())

class RecuperarForm(forms.Form):
    correo = forms.EmailField()

class PartidoForm(forms.ModelForm):
    class Meta:
        model = Partido
        fields = ['equipo_local', 'equipo_visitante', 'fecha_hora']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            equipos = Equipo.objects.filter(liga__administrador=user)
            self.fields['equipo_local'].queryset = equipos
            self.fields['equipo_visitante'].queryset = equipos
            
from django import forms
from .models import Apuesta

class ApuestaForm(forms.ModelForm):

    seleccion_ganador = forms.ChoiceField(
        choices=[],
        required=False
    )

    class Meta:
        model = Apuesta
        fields = ['tipo', 'seleccion_ganador', 'monto']

    def __init__(self, *args, **kwargs):
        self.partido = kwargs.pop('partido', None)
        self.usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)

        if self.partido:
            self.fields['seleccion_ganador'].choices = [
            ('local', self.partido.equipo_local.nombre),
            ('empate', 'Empate'),
            ('visitante', self.partido.equipo_visitante.nombre),
            ]


    def clean_monto(self):
        monto = self.cleaned_data.get('monto')

        if self.usuario and monto:
            saldo = self.usuario.perfil.saldo
            if monto > saldo:
                raise forms.ValidationError(
                    "Saldo insuficiente para realizar esta apuesta"
                )
        return monto

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')

        if tipo == 'ganador' and not cleaned_data.get('seleccion_ganador'):
            self.add_error('seleccion_ganador', 'Debe seleccionar un ganador')

        return cleaned_data