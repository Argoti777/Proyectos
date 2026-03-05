from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('campeonato/', views.campeonato, name='campeonato'),
    path('ayuda/', views.ayuda, name='ayuda'),
    path('Estadisticas_campeonato/', views.Estadisticas_campeonato, name='Estadisticas_campeonato'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('navbar/',views.navbar, name='navbar'),
    path('footer/',views.footer, name='footer'),
    path('registrar/', views.registrar, name='registrar'),
    path('signup/', views.registrar, name='signup'),
    path('login/', views.logon, name='login'),
    #URLs de administración
    path('crear/liga/', views.crear_liga, name='crear_liga'),
    path('crear/equipo/', views.crear_equipo, name='crear_equipo'),
    path('crear/jugador/', views.crear_jugador, name='crear_jugador'),
    path('adminis/', views.adminis, name='adminis'),
    path('navar_admin/', views.navbar_admin, name='navbar_admin'),
    path('chullagol/', views.chullagol, name='chullagol'),
    path('calendario_partidos/', views.prueba, name='prueba'),
    #URLs de funciones de busqueda
    path('equipo/<int:equipo_id>/', views.info_equipo, name='info_equipo'),
    path('liga/<int:liga_id>/', views.info_liga, name='info_liga'),
    path('jugador/<int:jugador_id>/', views.info_jugador, name='info_jugador'),
    path('buscar/', views.buscar, name='buscar'),
    path('buscar2/', views.buscar2, name='buscar2'),
    #URLs de edición y eliminación
    path('visualizar_liga/', views.visualizar_liga, name='visualizar_liga'),
    path('editar_liga/<int:liga_id>/', views.editar_liga, name='editar_liga'),
    path('liga/<int:liga_id>/eliminar/', views.eliminar_liga, name='eliminar_liga'),
    path('visualizar/equipo/', views.visualizar_equipo, name='visualizar_equipo'),
    path('editar/equipo/<int:equipo_id>/', views.editar_equipo, name='editar_equipo'),
    path('equipo/<int:equipo_id>/eliminar/', views.eliminar_equipo, name='eliminar_equipo'),
    path('visualizar/jugador/', views.visualizar_jugador, name='visualizar_jugador'),
    path('editar/jugador/<int:jugador_id>/', views.editar_jugador, name='editar_jugador'),
    path('jugador/<int:jugador_id>/eliminar/', views.eliminar_jugador, name='eliminar_jugador'),

    #URLs de apuestas
    path("apostar/<int:partido_id>/", views.apostar, name="apostar"),
    path("apuesta-exitosa/", views.apuesta_exitosa, name="apuesta_exitosa"),
    path("mis_apuestas/", views.historial_apuestas, name="historial_apuestas"),
    
    #URLs de administración de partidos
    path('administrar_partido/<int:partido_id>/', views.administrar_partido, name='administrar_partido'),
    path('mi_partido/', views.mi_partido, name='mi_partido'),
    path('administrar_partido/<int:partido_id>/iniciar/',views.iniciar_partido,name='iniciar_partido'),
    path('administrar_partido/<int:partido_id>/finalizar/',views.finalizar_partido,name='finalizar_partido'),
    path('administrar_partido/<int:partido_id>/gol/<str:equipo>/',views.anotar_gol,name='anotar_gol'),
    path('administrar_partido/<int:partido_id>/evento/',views.registrar_evento,name='registrar_evento'),
    
    path('recargar_saldo/', views.recargar_saldo, name='recargar_saldo'),
    
    path('partido/<int:partido_id>/abrir-apuestas/',views.abrir_apuestas_partido,name='abrir_apuestas_partido'),

    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

