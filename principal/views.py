from django.shortcuts import render


def home(request):
    return render(request, 'principal/home.html')

def campeonato(request):
    return render(request, 'principal/campeonato.html')

def ayuda(request):
    return render(request, 'principal/ayuda.html')

def inicio_sesion(request):
    return render(request, 'principal/inicio_sesion.html')  

# Create your views here.