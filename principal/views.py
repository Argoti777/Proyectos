from django.shortcuts import render


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
# Create your views here.