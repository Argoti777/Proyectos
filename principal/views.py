from django.shortcuts import render


def home(request):
    return render(request, 'principal/home.html')

def campeonato(request):
    return render(request, 'principal/campeonato.html')

def ayuda(request):
    return render(request, 'principal/ayuda.html')

# Create your views here.