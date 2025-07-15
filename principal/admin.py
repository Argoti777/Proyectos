from django.contrib import admin
from .models import Usuario, Liga, Equipo, Jugador, Partido, EventoPartido


admin.site.register(Usuario)
admin.site.register(Liga)
admin.site.register(Equipo)
admin.site.register(Jugador)
admin.site.register(Partido)
admin.site.register(EventoPartido)