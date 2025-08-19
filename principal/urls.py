from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('campeonato/', views.campeonato, name='campeonato'),
    path('ayuda/', views.ayuda, name='ayuda'),
    path('inicio_sesion/', views.inicio_sesion, name='inicio_sesion'),
    path('detalle_partido/', views.detalle_partido, name='detalle_partido'),
    path('Estadisticas_campeonato/', views.Estadisticas_campeonato, name='Estadisticas_campeonato'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('navbar/',views.navbar, name='navbar'),
    path('footer/',views.footer, name='footer'),
    path('perfil/', views.perfil, name='perfil'),
    path('chullagol/', views.chullagol, name='chullagol'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

