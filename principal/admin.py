from django.contrib import admin
from .models import User, Liga, Equipo, Jugador, Partido, EventoPartido, Noticia

admin.site.register(Liga)
admin.site.register(Equipo)
admin.site.register(Jugador)
admin.site.register(Partido)
admin.site.register(EventoPartido)
admin.site.register(Noticia)
