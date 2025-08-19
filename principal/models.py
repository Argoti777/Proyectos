from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.



class Liga(models.Model):
    nombre = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    administrador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ligas')

    class Meta:
        db_table = "Ligas"

    def __str__(self):
        return self.nombre


class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    liga = models.ForeignKey(Liga, on_delete=models.CASCADE, related_name='equipos')
    logo = models.ImageField(upload_to='equipos/', null=True, blank=True)
    class Meta:
        db_table = "Equipos"

    def __str__(self):
        return self.nombre


class Jugador(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    edad = models.IntegerField()
    posicion = models.CharField(max_length=50)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='jugadores')
    foto = models.ImageField(upload_to='jugadores/', null=True, blank=True)
    class Meta:
        db_table = "Jugadores"

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Partido(models.Model):
    equipo_local = models.ForeignKey(Equipo, related_name='partidos_locales', on_delete=models.CASCADE)
    equipo_visitante = models.ForeignKey(Equipo, related_name='partidos_visitantes', on_delete=models.CASCADE)
    liga = models.ForeignKey(Liga, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField()
    goles_local = models.IntegerField(default=0)
    goles_visitante = models.IntegerField(default=0)
    estado = models.CharField(max_length=50)  # 'programado', 'en_juego', 'finalizado'

    class Meta:
        db_table = "Partidos"

    def __str__(self):
        return f"{self.equipo_local} vs {self.equipo_visitante} ({self.fecha_hora})"


class EventoPartido(models.Model):
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE, related_name='eventos')
    jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE, related_name='eventos')
    tipo_evento = models.CharField(max_length=50)  # gol, tarjeta_amarilla, tarjeta_roja, etc.
    minuto = models.IntegerField()
    detalle = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "EventosPartidos"

    def __str__(self):
        return f"{self.tipo_evento} - {self.jugador} - {self.minuto} min"
