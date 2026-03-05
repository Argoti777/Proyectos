from decimal import Decimal
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
# Create your models here.


class Liga(models.Model):
    nombre = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True, max_length=2000)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    administrador = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='ligas')

    class Meta:
        db_table = "Ligas"

    def __str__(self):
        return self.nombre


class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    liga = models.ForeignKey(
        Liga, on_delete=models.CASCADE, related_name='equipos')
    logo = models.ImageField(upload_to='equipos/', null=True, blank=True)

    class Meta:
        db_table = "Equipos"

    def __str__(self):
        return self.nombre


class Jugador(models.Model):
    cedula = models.CharField(
        max_length=10, unique=True, verbose_name="Cédula")
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    edad = models.IntegerField()
    posicion = models.CharField(max_length=50)
    equipo = models.ForeignKey(
        Equipo, on_delete=models.CASCADE, related_name='jugadores')
    foto = models.ImageField(upload_to='jugadores/', null=True, blank=True)

    class Meta:
        db_table = "Jugadores"

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.cedula}"


class Partido(models.Model):
    liga = models.ForeignKey(
        Liga, on_delete=models.CASCADE, related_name='partidos')
    equipo_local = models.ForeignKey(
        Equipo, related_name='partidos_locales', on_delete=models.CASCADE)
    equipo_visitante = models.ForeignKey(
        Equipo, related_name='partidos_visitantes', on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(default=timezone.now)
    goles_local = models.IntegerField(default=0)
    goles_visitante = models.IntegerField(default=0)
    administrador = models.ForeignKey(User, on_delete=models.CASCADE)
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('en_juego', 'En juego'),
        ('finalizado', 'Finalizado'),
    ]
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='pendiente'
    )

    class Meta:
        db_table = "Partidos"

    def __str__(self):
        return f"{self.equipo_local.nombre} vs {self.equipo_visitante.nombre}"

    def guardar_resultado(self):
        """
        Método que actualiza automáticamente la tabla de posiciones
        después de que un partido es finalizado.
        """
        if self.estado != 'finalizado':
            return  # Solo actualiza si ya terminó el partido

        # Obtener o crear estadísticas de los dos equipos
        estadistica_local, _ = Estadistica.objects.get_or_create(
            equipo=self.equipo_local, liga=self.liga)
        estadistica_visitante, _ = Estadistica.objects.get_or_create(
            equipo=self.equipo_visitante, liga=self.liga)

        # Actualizar los valores
        estadistica_local.partidos_jugados += 1
        estadistica_visitante.partidos_jugados += 1

        estadistica_local.goles_favor += self.goles_local
        estadistica_local.goles_contra += self.goles_visitante
        estadistica_visitante.goles_favor += self.goles_visitante
        estadistica_visitante.goles_contra += self.goles_local

        # Resultado del partido
        if self.goles_local > self.goles_visitante:
            estadistica_local.partidos_ganados += 1
            estadistica_local.puntos += 3
            estadistica_visitante.partidos_perdidos += 1
        elif self.goles_local < self.goles_visitante:
            estadistica_visitante.partidos_ganados += 1
            estadistica_visitante.puntos += 3
            estadistica_local.partidos_perdidos += 1
        else:
            estadistica_local.partidos_empatados += 1
            estadistica_visitante.partidos_empatados += 1
            estadistica_local.puntos += 1
            estadistica_visitante.puntos += 1

        estadistica_local.save()
        estadistica_visitante.save()


class Cuota(models.Model):
    partido = models.OneToOneField(Partido, on_delete=models.CASCADE)
    local = models.FloatField()
    empate = models.FloatField()
    visitante = models.FloatField()
    activa = models.BooleanField(default=False)  # 👈 NUEVO

    class Meta:
        db_table = "Cuotas"

    def __str__(self):
        estado = "Activa" if self.activa else "Inactiva"
        return f"Cuotas {estado} de {self.partido}"


class Apuesta(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE)

    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('ganada', 'Ganada'),
        ('perdida', 'Perdida'),
    ]

    estado = models.CharField(
        max_length=10,
        choices=ESTADOS,
        default='pendiente'
    )
    tipo = models.CharField(max_length=20, choices=[
        ('ganador', 'Ganador'),
    ])

    # GANADOR: local / empate / visitante
    seleccion_ganador = models.CharField(
        max_length=20, blank=True, null=True
    )

    # OVER/UNDER
    over_under = models.CharField(
        max_length=10,
        choices=[('over', 'Más de'), ('under', 'Menos de')],
        blank=True,
        null=True
    )
    linea_goles = models.FloatField(blank=True, null=True)  # ejemplo: 2.5
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    
    def es_ganadora(self):
        partido = self.partido

        # Solo evaluar si el partido terminó
        if partido.estado != 'finalizado':
            return False

        # 🔹 Apuesta tipo GANADOR
        if self.tipo == 'ganador':
            if partido.goles_local > partido.goles_visitante:
                resultado = 'local'
            elif partido.goles_local < partido.goles_visitante:
                resultado = 'visitante'
            else:
                resultado = 'empate'

            return self.seleccion_ganador == resultado

        # 🔹 Apuesta tipo OVER / UNDER
        elif self.tipo == 'overunder':
            total_goles = partido.goles_local + partido.goles_visitante

            if self.over_under == 'over':
                return total_goles > self.linea_goles
            elif self.over_under == 'under':
                return total_goles < self.linea_goles

        return False
    
    def calcular_ganancia(self):
        cuota = self.partido.cuota

        if self.tipo == 'ganador':
            if self.seleccion_ganador == 'local':
                return self.monto * Decimal(cuota.local)
            elif self.seleccion_ganador == 'empate':
                return self.monto * Decimal(cuota.empate)
            elif self.seleccion_ganador == 'visitante':
                return self.monto * Decimal(cuota.visitante)

    # Puedes ampliar lógica para over/under si luego agregas cuotas

        return Decimal(0)

    class Meta:
        db_table = "Apuestas"

    def __str__(self):
        return f"Apuesta de {self.usuario.username} en {self.partido}"
    


class Estadistica(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    liga = models.ForeignKey(Liga, on_delete=models.CASCADE)
    partidos_jugados = models.IntegerField(default=0)
    partidos_ganados = models.IntegerField(default=0)
    partidos_empatados = models.IntegerField(default=0)
    partidos_perdidos = models.IntegerField(default=0)
    goles_favor = models.IntegerField(default=0)
    goles_contra = models.IntegerField(default=0)
    puntos = models.IntegerField(default=0)

    class Meta:
        unique_together = ('equipo', 'liga')
        ordering = ['-puntos', '-goles_favor']

    def __str__(self):
        return f"{self.equipo.nombre} - {self.liga.nombre}"

    @property
    def diferencia_goles(self):
        return self.goles_favor - self.goles_contra


class EventoPartido(models.Model):
    partido = models.ForeignKey(
        Partido, on_delete=models.CASCADE, related_name='eventos')
    jugador = models.ForeignKey(
        Jugador, on_delete=models.CASCADE, related_name='eventos')
    # gol, tarjeta_amarilla, tarjeta_roja, etc.
    tipo_evento = models.CharField(max_length=50)
    minuto = models.IntegerField()
    detalle = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "EventosPartidos"

    def __str__(self):
        return f"{self.tipo_evento} - {self.jugador} - {self.minuto} min"


class Perfil(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    saldo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=100.00  # saldo inicial ficticio
    )

    def __str__(self):
        return f"{self.usuario.username} - Saldo: {self.saldo}"


class MovimientoSaldo(models.Model):
    TIPOS = (
        ('recarga', 'Recarga'),
        ('apuesta', 'Apuesta'),
        ('premio', 'Premio'),
    )

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.tipo} - {self.monto}"

class EloEquipo(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    liga = models.ForeignKey(Liga, on_delete=models.CASCADE)
    rating = models.FloatField(default=1200)
    partidos_jugados = models.IntegerField(default=0)

    class Meta:
        unique_together = ('equipo', 'liga')
        db_table = "EloEquipos"

    def __str__(self):
        return f"{self.equipo.nombre} ({self.liga.nombre}) - {self.rating:.1f}"


class PartidoHistoricoMLP(models.Model):
    partido = models.OneToOneField(
        Partido, on_delete=models.CASCADE, unique=True
    )
    liga = models.ForeignKey(Liga, on_delete=models.CASCADE)

    elo_local = models.FloatField()
    elo_visitante = models.FloatField()
    diff_elo = models.FloatField()

    partidos_local = models.IntegerField()
    partidos_visitante = models.IntegerField()

    resultado = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "PartidosHistoricosMLP"


class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ['-fecha_publicacion']
        db_table = "Noticias"

    def __str__(self):
        return self.titulo
