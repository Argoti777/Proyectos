from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('campeonato/', views.campeonato, name='campeonato'),
    path('ayuda/', views.ayuda, name='ayuda'),
    path('inicio_sesion/', views.inicio_sesion, name='inicio_sesion'),
    path('detalle_partido/', views.detalle_partido, name='detalle_partido'),
    path('Estadisticas_campeonato/', views.Estadisticas_campeonato, name='Estadisticas_campeonato'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('base/',views.base, name='base'),
    path('navbar/',views.navbar, name='navbar'),
    path('footer/',views.footer, name='footer'),
]


