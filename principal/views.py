from django.shortcuts import render
from django.shortcuts import render, redirect

def home(request):
    return render(request, 'principal/home.html')

def campeonato(request):
    return render(request, 'principal/campeonato.html')

def ayuda(request):
    return render(request, 'principal/ayuda.html')

def inicio_sesion(request):
    return render(request, 'principal/inicio_sesion.html')  

def detalle_partido(request):
    return render(request, 'principal/detalle_partido.html')

def estadisticas_partido(request):
    return render(request, 'principal/estadisticas_partido.html')

def Estadisticas_campeonato(request):
    return render(request, 'principal/Estadisticas_campeonato.html')

def navbar(request):
    return render(request,'principal/navbar.html')

def footer(request):
    return render(request,'principal/footer.html')

def perfil(request):
    return render(request,'principal/perfil.html')

# Create your views here.

from .forms import *
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import Usuario
from django.db.models import Q

def inicio_sesion(request):
    registro_form = RegistroForm()
    login_form = LoginForm()
    recuperar_form = RecuperarForm()
    if request.method == 'POST':
        if 'registrarse' in request.POST:
            registro_form = RegistroForm(request.POST)
            if registro_form.is_valid():
                usuario = registro_form.save(commit=False)
                usuario.contraseña = make_password(registro_form.cleaned_data['contraseña'])
                usuario.save()
                messages.success(request, 'Cuenta creada exitosamente. ¡Inicia sesión!')
                return redirect('inicio_sesion')
        elif 'iniciar_sesion' in request.POST:
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                dato = login_form.cleaned_data['correo_o_numero']
                contraseña = login_form.cleaned_data['contraseña']
                try:
                    usuario = Usuario.objects.get(
                        Q(correo=dato) | Q(numero=dato)
                    )
                    if check_password(contraseña, usuario.contraseña):
                        # GUARDAR DATOS EN SESIÓN
                        request.session['usuario_id'] = usuario.id
                        request.session['usuario_nombre'] = usuario.nombre
                        messages.success(request, f'Bienvenido {usuario.nombre}')
                        return redirect('home')  # Cambia 'inicio' por tu vista principal
                    else:
                        messages.error(request, 'Contraseña incorrecta.')
                except Usuario.DoesNotExist:
                    messages.error(request, 'Usuario no encontrado.')
        # Recuperar contraseña (si tienes lógica)
        elif 'recuperar' in request.POST:
            recuperar_form = RecuperarForm(request.POST)
            # Tu lógica...

    context = {
        'registro_form': registro_form,
        'login_form': login_form,
        'recuperar_form': recuperar_form,
    }
    return render(request, 'principal/inicio_sesion.html', context)

def cerrar_sesion(request):
    request.session.flush()
    return redirect('home')

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Perfil
from .forms import PerfilForm

def perfil(request):
    # Obtener o crear el perfil del usuario autenticado
    perfil, creado = Perfil.objects.get_or_create(usuario=request.user)

    if request.method == 'POST':
        perfil_form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if perfil_form.is_valid():
            perfil_form.save()
            return redirect('perfil')  # O donde quieras redirigir después de guardar
    else:
        perfil_form = PerfilForm(instance=perfil)

    return render(request, "principal/perfil.html", {"perfil_form": perfil_form})

#Prueba de paso de datos de campeonato
from django.shortcuts import render
from .models import Jugador, Equipo, Liga

def campeonato(request):
    jugadores = Jugador.objects.all()
    equipos = Equipo.objects.all()
    ligas = Liga.objects.all()
    return render(request, 'principal/campeonato.html', {
        'jugadores': jugadores,
        'equipos': equipos,
        'ligas': ligas,
    })