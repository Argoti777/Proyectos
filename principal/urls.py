from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('campeonato/', views.campeonato, name='campeonato'),
    path('ayuda/', views.ayuda, name='ayuda'),
    path('inicio_sesion/', views.inicio_sesion, name='inicio_sesion'),
    path('detalle_partido/', views.detalle_partido, name='detalle_partido'),
    path('Estadisticas_campeonato/', views.Estadisticas_campeonato, name='Estadisticas_campeonato'),
]

