from django.contrib.auth.decorators import login_required
from .models import Jugador, Equipo, Liga, User
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from .forms import *
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout


def inicio_sesion(request):
    if request.method == 'GET':
        return render(request, 'principal/inicio_sesion.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            # registar user
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except:
                return render(request, 'principal/inicio_sesion.html', {
                    'form': UserCreationForm(),
                    'error': 'El usuario ya existe'})
        return render(request, 'principal/inicio_sesion.html', {
            'form': UserCreationForm(),
            'error': 'Las contraseñas no coinciden'})

def crear_liga(request):
    if request.method == 'GET':
        return render(request, 'principal/crear_liga.html', {
            'form': crearLigaForm()
        })
    else:
        try:
            form = crearLigaForm(request.POST)
            nueva_liga = form.save(commit=False)
            nueva_liga.administrador = request.user
            nueva_liga.save()
            return redirect('crear_liga')
        except ValueError:
            return render(request, 'principal/crear_liga.html', {
                'form': crearLigaForm(),
                'error': 'Por favor ingrese datos válidos'
            })
            
def crear_equipo(request):
    if request.method == 'GET':
        return render(request, 'principal/crear_equipo.html', {
            'form': crearEquipoForm()
        })
    else:
        try:
            form = crearEquipoForm(request.POST)
            nuevo_equipo = form.save(commit=False)
            nuevo_equipo.administrador = request.user
            nuevo_equipo.save()
            return redirect('crear_equipo')
        except ValueError:
            return render(request, 'principal/crear_equipo.html', {
                'form': crearEquipoForm(),
                'error': 'Por favor ingrese datos válidos'
            })

def crear_jugador(request):
    if request.method == 'GET':
        return render(request, 'principal/crear_jugador.html', {
            'form': crearJugadorForm()
        })
    else:
        try:
            form = crearJugadorForm(request.POST)
            nuevo_jugador = form.save(commit=False)
            nuevo_jugador.administrador = request.user
            nuevo_jugador.save()
            return redirect('crear_jugador')
        except ValueError:
            return render(request, 'principal/crear_jugador.html', {
                'form': crearJugadorForm(),
                'error': 'Por favor ingrese datos válidos'
            })

def cerrar_sesion(request):
    logout(request)
    return redirect('home')

def logon(request):
    if request.method == 'GET':
        return render(request, 'principal/login.html', {
            'form': AuthenticationForm()
            })
    else:
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password'])
        if user is None:
            return render(request, 'principal/login.html', {
                'form': AuthenticationForm(),
                'error': 'Usuario o contraseña incorrectos'})
        else:
            login(request, user)
            return redirect('home')
        



def home(request):
    return render(request, 'principal/home.html')
def campeonato(request):
    return render(request, 'principal/campeonato.html')
def ayuda(request):
    return render(request, 'principal/ayuda.html')
def detalle_partido(request):
    return render(request, 'principal/detalle_partido.html')
def estadisticas_partido(request):
    return render(request, 'principal/estadisticas_partido.html')
def Estadisticas_campeonato(request):
    return render(request, 'principal/Estadisticas_campeonato.html')
def navbar(request):
    return render(request, 'principal/navbar.html')
def footer(request):
    return render(request, 'principal/footer.html')
def adminis(request):
    return render(request, 'principal/adminis.html')
def navbar_admin(request):
    return render(request, 'principal/navbar_admin.html')
def chullagol(request):
    return render(request, 'principal/chullagol.html') 
# Prueba de paso de datos de campeonato
def campeonato(request):
    jugadores = Jugador.objects.all()
    equipos = Equipo.objects.all()
    ligas = Liga.objects.all()
    return render(request, 'principal/campeonato.html', {
        'jugadores': jugadores,
        'equipos': equipos,
        'ligas': ligas,
    })
