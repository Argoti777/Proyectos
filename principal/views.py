from django.contrib.admin.views.decorators import staff_member_required
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import *
from .models import Jugador, Equipo, Liga, Partido
import random
from datetime import datetime, timedelta, time
from itertools import combinations
from django.db import transaction
# Funcion para negar el acceso a usuarios que no son superusuarios


def superuser_required(view_func):
    decorated_view_func = user_passes_test(
        lambda u: u.is_active and u.is_superuser,
        login_url='home'  # redirige si no es superuser
    )(view_func)
    return decorated_view_func


def registrar(request):
    if request.method == 'GET':
        return render(request, 'principal/registrar.html', {'form': UserCreationForm()})

    else:
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

        # Si hay errores, el formulario los muestra automáticamente
        return render(request, 'principal/registrar.html', {
            'form': form,
        })


def cerrar_sesion(request):
    logout(request)
    return redirect('home')


def logon(request):
    if request.method == 'GET':
        return render(request, 'principal/login.html', {
            'form': AuthenticationForm()
        })
    else:
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password'])
        if user is None:
            return render(request, 'principal/login.html', {
                'form': AuthenticationForm(),
                'error': 'Usuario o contraseña incorrectos'})
        else:
            login(request, user)
            return redirect('home')

from .models import Noticia

def home(request):
    ligas = Liga.objects.all()
    liga_id = request.GET.get('liga')
    noticias = Noticia.objects.filter(activa=True)[:6]

    if liga_id:
        liga_seleccionada = Liga.objects.filter(id=liga_id).first()
    else:
        liga_seleccionada = ligas.first()

    tabla_posiciones = []

    if liga_seleccionada:
        tabla_posiciones = Estadistica.objects.filter(
            liga=liga_seleccionada
        ).select_related('equipo')

    context = {
        'ligas': ligas,
        'liga_seleccionada': liga_seleccionada,
        'tabla_posiciones': tabla_posiciones,
        'noticias': noticias
    }

    return render(request, 'principal/home.html', context)


def ayuda(request):
    return render(request, 'principal/ayuda.html')


def estadisticas_partido(request):
    return render(request, 'principal/estadisticas_partido.html')


def Estadisticas_campeonato(request):
    return render(request, 'principal/Estadisticas_campeonato.html')


def navbar(request):
    return render(request, 'principal/navbar.html')


def footer(request):
    return render(request, 'principal/footer.html')


def campeonato(request):
    jugadores = Jugador.objects.all()[:6]
    equipos = Equipo.objects.all()[:6]
    ligas = Liga.objects.all()[:9]
    return render(request, 'principal/campeonato.html', {
        'jugadores': jugadores,
        'equipos': equipos,
        'ligas': ligas,
    })


def buscar(request):
    query = request.GET.get('q')
    jugadores = Jugador.objects.filter(
        Q(nombre__icontains=query) | Q(apellido__icontains=query)
    )
    equipos = Equipo.objects.filter(
        Q(nombre__icontains=query) | Q(ciudad__icontains=query)
    )
    ligas = Liga.objects.filter(
        Q(nombre__icontains=query) | Q(
            pais__icontains=query) | Q(ciudad__icontains=query)
    )
    return render(request, 'principal/campeonato.html', {
        'jugadores': jugadores,
        'equipos': equipos,
        'ligas': ligas,
        'query': query
    })


def info_liga(request, liga_id):
    liga = get_object_or_404(Liga, id=liga_id)
    return render(request, 'principal/info_liga.html', {'liga': liga})


def info_equipo(request, equipo_id):
    equipo = get_object_or_404(Equipo, id=equipo_id)
    return render(request, 'principal/info_equipo.html', {'equipo': equipo})


def info_jugador(request, jugador_id):
    jugador = get_object_or_404(Jugador, cedula=jugador_id)
    return render(request, 'principal/info_jugador.html', {'jugador': jugador})


@login_required
def chullagol(request):
    form = ApuestaForm()
    partidos = (Partido.objects.filter(
        fecha_hora__gt=timezone.now(),
        estado='pendiente'
    )
    .order_by('fecha_hora')[:12]
)

    return render(request, 'principal/chullagol.html', {
        'partidos': partidos,
        'form': form
    })

from principal.services.mlp_inferencia import probabilidades_mlp
from principal.models import Cuota
from django.contrib import messages

@login_required
@transaction.atomic
def apostar(request, partido_id):
    partido = get_object_or_404(Partido, id=partido_id)
    
    if not hasattr(partido, 'cuota') or not partido.cuota.activa:
        return render(request, "principal/apuesta_bloqueada.html", {
        "mensaje": "Las apuestas aún no están abiertas para este partido"
        })

    # Partido finalizado
    if partido.estado == 'finalizado':
        return render(request, "principal/apuesta_bloqueada.html", {
            "partido": partido,
            "mensaje": "Este partido ya finalizó"
        })

    # Partido ya empezó
    if partido.fecha_hora <= timezone.now():
        return render(request, "principal/apuesta_bloqueada.html", {
            "partido": partido,
            "mensaje": "El partido ya comenzó"
        })

    if request.method == "POST":
        form = ApuestaForm(
            request.POST,
            partido=partido,
            usuario=request.user
        )

        if form.is_valid():
            apuesta = form.save(commit=False)
            apuesta.usuario = request.user
            apuesta.partido = partido
            apuesta.estado = 'pendiente'
            apuesta.save()

            # 💸 Descontar saldo
            perfil = request.user.perfil
            perfil.saldo -= apuesta.monto
            perfil.save()

            # 🧾 Registrar movimiento
            MovimientoSaldo.objects.create(
                usuario=request.user,
                tipo='apuesta',
                monto=-apuesta.monto,
                descripcion=f"Apuesta partido {partido.id}"
            )

            messages.success(request, "✅ Apuesta realizada con éxito")
            return redirect("chullagol")

    else:
        form = ApuestaForm(
            partido=partido,
            usuario=request.user
        )
        
    cuota = Cuota.objects.filter(partido=partido).first()

    probs = probabilidades_mlp(partido)


    return render(request, "principal/apostar.html", {
        "partido": partido,
        "form": form,
        "cuota": cuota,
        "probs": probs
    })




@login_required
def apuesta_exitosa(request):
    return render(request, "principal/apuesta_exitosa.html")


@login_required
def historial_apuestas(request):
    apuestas = Apuesta.objects.filter(usuario=request.user).order_by('-fecha')

    return render(request, "principal/historial_apuestas.html", {
        "apuestas": apuestas
    })

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
# Vistas para administrador

@staff_member_required
def buscar2(request):
    query = request.GET.get('q')
    tipo = request.GET.get('tipo')  # Saber desde dónde se busca

    jugadores = Jugador.objects.filter(
        Q(nombre__icontains=query) | Q(apellido__icontains=query)
    )
    equipos = Equipo.objects.filter(
        Q(nombre__icontains=query) | Q(ciudad__icontains=query)
    )
    ligas = Liga.objects.filter(
        Q(nombre__icontains=query) | Q(
            pais__icontains=query) | Q(ciudad__icontains=query)
    )

    if tipo == 'equipo':
        template = 'principal/visualizar_equipo.html'
        context = {'equipos': equipos, 'query': query}
    elif tipo == 'jugador':
        template = 'principal/visualizar_jugador.html'
        context = {'jugadores': jugadores, 'query': query}
    else:  # Por defecto, liga
        template = 'principal/visualizar_liga.html'
        context = {'ligas': ligas, 'query': query}

    return render(request, template, context)


@staff_member_required
def crear_liga(request):
    if request.method == 'GET':
        return render(request, 'principal/crear_liga.html', {
            'form': crearLigaForm()
        })
    else:
        form = crearLigaForm(request.POST)
        if form.is_valid():
            nueva_liga = form.save(commit=False)
            nueva_liga.administrador = request.user
            nueva_liga.save()
            return redirect('crear_liga')
        else:
            return render(request, 'principal/crear_liga.html', {
                'form': form
            })


@login_required
@staff_member_required
def visualizar_liga(request):
    # Filtrar solo las ligas que le pertenecen al usuario logueado
    ligas = Liga.objects.filter(administrador=request.user)[:12]
    return render(request, 'principal/visualizar_liga.html', {
        'ligas': ligas,
    })


@staff_member_required
def editar_liga(request, liga_id):
    liga = get_object_or_404(Liga, id=liga_id)

    if request.method == 'POST':
        form = crearLigaForm(request.POST, instance=liga)
        if form.is_valid():
            form.save()
            # te devuelve a actualizar_liga.html
            return redirect('visualizar_liga')
    else:
        form = crearLigaForm(instance=liga)

    return render(request, 'principal/editar_liga.html', {'form': form, 'liga': liga})


@staff_member_required
def eliminar_liga(request, liga_id):
    liga = get_object_or_404(Liga, id=liga_id)

    if request.method == "POST":  # Solo eliminar si es POST (más seguro)
        liga.delete()
        return redirect('visualizar_liga')  # Redirige a la lista de equipos

    # Si es GET, mostramos una confirmación
    return render(request, 'principal/confirmar_eliminar.html', {'liga': liga})


@staff_member_required
def crear_equipo(request):
    if request.method == 'GET':
        return render(request, 'principal/crear_equipo.html', {
            'form': crearEquipoForm(user=request.user)
        })
    else:
        try:
            form = crearEquipoForm(request.POST, user=request.user)  # ojo aquí
            nuevo_equipo = form.save(commit=False)
            nuevo_equipo.administrador = request.user
            nuevo_equipo.save()
            return redirect('crear_equipo')
        except ValueError:
            return render(request, 'principal/crear_equipo.html', {
                'form': crearEquipoForm(user=request.user),
                'error': 'Por favor ingrese datos válidos'
            })


@staff_member_required
def visualizar_equipo(request):
    equipos = Equipo.objects.filter(liga__administrador=request.user)[:12]
    return render(request, 'principal/visualizar_equipo.html', {
        'equipos': equipos,
    })


@staff_member_required
def editar_equipo(request, equipo_id):
    equipo = get_object_or_404(Equipo, id=equipo_id)

    if request.method == 'POST':
        form = crearEquipoForm(request.POST, instance=equipo)
        if form.is_valid():
            form.save()
            # te devuelve a actualizar_equipo.html
            return redirect('visualizar_equipo')
    else:
        form = crearEquipoForm(instance=equipo)

    return render(request, 'principal/editar_equipo.html', {'form': form, 'equipo': equipo})


@staff_member_required
def eliminar_equipo(request, equipo_id):
    equipo = get_object_or_404(Equipo, id=equipo_id)

    if request.method == "POST":  # Solo eliminar si es POST (más seguro)
        equipo.delete()
        return redirect('visualizar_equipo')  # Redirige a la lista de equipos

    # Si es GET, mostramos una confirmación
    return render(request, 'principal/confirmar_eliminar.html', {'equipo': equipo})


@staff_member_required
def crear_jugador(request):
    if request.method == 'GET':
        return render(request, 'principal/crear_jugador.html', {
            'form': crearJugadorForm(user=request.user)
        })
    else:
        try:
            form = crearJugadorForm(
                request.POST, user=request.user)  # ojo aquí)
            nuevo_jugador = form.save(commit=False)
            nuevo_jugador.administrador = request.user
            nuevo_jugador.save()
            return redirect('crear_jugador')
        except ValueError:
            return render(request, 'principal/crear_jugador.html', {
                'form': crearJugadorForm(user=request.user),
                'error': 'Por favor ingrese datos válidos'
            })


@staff_member_required
def visualizar_jugador(request):
    jugadores = Jugador.objects.filter(
        equipo__liga__administrador=request.user)[:12]
    return render(request, 'principal/visualizar_jugador.html', {
        'jugadores': jugadores,
    })


@staff_member_required
def editar_jugador(request, jugador_id):
    jugador = get_object_or_404(Jugador, cedula=jugador_id)

    if request.method == 'POST':
        form = crearJugadorForm(request.POST, instance=jugador)
        if form.is_valid():
            form.save()
            # te devuelve a actualizar_jugador.html
            return redirect('visualizar_jugador')
    else:
        form = crearJugadorForm(instance=jugador)

    return render(request, 'principal/editar_jugador.html', {'form': form, 'jugador': jugador})


@staff_member_required
def eliminar_jugador(request, jugador_id):
    jugador = get_object_or_404(Jugador, cedula=jugador_id)

    if request.method == "POST":  # Solo eliminar si es POST (más seguro)
        jugador.delete()
        return redirect('visualizar_jugador')  # Redirige a la lista de equipos

    # Si es GET, mostramos una confirmación
    return render(request, 'principal/confirmar_eliminar.html', {'jugador': jugador})


@staff_member_required
def adminis(request):
    return render(request, 'principal/adminis.html')


@staff_member_required
def navbar_admin(request):
    return render(request, 'principal/navbar_admin.html')

from .services.elo import probabilidades_partido
from .models import Cuota
from .services.cuotas import crear_cuotas_para_partido
@staff_member_required
def prueba(request):

    ligas = Liga.objects.filter(administrador=request.user)
    equipos = Equipo.objects.filter(liga__administrador=request.user)
    partidos_generados = []

    if request.method == 'POST':
        tipo = request.POST.get('tipo_partido')  # 'campeonato'
        liga_id = request.POST.get('liga')
        # 'round_robin' o 'idas_antes_vueltas'
        modo = request.POST.get('modo', 'round_robin')
        # si viene 'on' mezclamos aleatoriamente
        aleatorio = request.POST.get('aleatorio') == 'on'

        if not liga_id:
            return render(request, 'principal/prueba.html', {
                'ligas': ligas,
                'equipos': equipos,
                'error': 'Por favor selecciona una liga.'
            })

        liga = get_object_or_404(Liga, id=liga_id)
        
        from django.utils import timezone
        
        hoy = timezone.now().date()

        liga_activa = liga.fecha_inicio <= hoy <= liga.fecha_fin

        ya_tiene_partidos = Partido.objects.filter(liga=liga).exists()

        if liga_activa and ya_tiene_partidos:
            return render(request, 'principal/prueba.html', {
                'ligas': ligas,
                'equipos': equipos,
                'error': 'Esta liga ya tiene un campeonato activo. Solo podrás generar otro cuando finalice.'
            })
        
        if tipo != 'campeonato':
            return render(request, 'principal/prueba.html', {
                'ligas': ligas,
                'equipos': equipos,
                'error': 'Solo está disponible la generación de calendario para campeonato por puntos.'
            })

        equipos_liga = list(Equipo.objects.filter(liga=liga))

        if len(equipos_liga) < 2:
            return render(request, 'principal/prueba.html', {
                'ligas': ligas,
                'equipos': equipos,
                'error': 'Se necesitan al menos 2 equipos para generar un campeonato.'
            })

        fecha_inicio = liga.fecha_inicio
        fecha_fin = liga.fecha_fin
        dias_totales = (fecha_fin - fecha_inicio).days + 1
        if dias_totales <= 0:
            return render(request, 'principal/prueba.html', {
                'ligas': ligas,
                'equipos': equipos,
                'error': 'La fecha de fin debe ser posterior o igual a la fecha de inicio de la liga.'
            })

        # ---------- Generadores de emparejamientos ----------

        def round_robin_rounds(teams):
            """Genera una lista de jornadas (cada jornada = lista de pares) usando el método 'circle'."""
            t = teams[:]
            if len(t) % 2 == 1:
                t.append(None)  # bye
            n = len(t)
            rounds = []
            for r in range(n - 1):
                pairs = []
                for i in range(n // 2):
                    a = t[i]
                    b = t[n - 1 - i]
                    if a is None or b is None:
                        continue
                    # alternamos local/visitante por jornada para balancear casas
                    if r % 2 == 0:
                        pairs.append((a, b))
                    else:
                        pairs.append((b, a))
                rounds.append(pairs)
                # rotación (mantener cabeza fija)
                t = [t[0]] + [t[-1]] + t[1:-1]
            return rounds

        # Modo 1: round-robin por jornadas (cada equipo juega 1 vez por jornada)
        if modo == 'round_robin':
            jornadas = round_robin_rounds(equipos_liga)
            # aplanamos las jornadas en orden: jornada1, jornada2, ...
            partidos_lista = [par for jornada in jornadas for par in jornada]
            # Añadimos la vuelta (inverso) al final, si queremos ida y vuelta:
            vuelta = [(v, u) for (u, v) in partidos_lista]
            partidos_lista = partidos_lista + vuelta

        # Modo 2: todas las idas primero (pares combinatorios, pero evitando la lista "fija" 1 vs todos)
        elif modo == 'idas_antes_vueltas':
            # creamos pares (una ida y luego la vuelta), pero ordenamos las idas usando round-robin para evitar 1vsN secuenciales
            jornadas = round_robin_rounds(equipos_liga)
            round1 = [par for jornada in jornadas for par in jornada]
            round2 = [(v, u) for (u, v) in round1]
            partidos_lista = round1 + round2

        else:
            # modo por defecto: round_robin
            jornadas = round_robin_rounds(equipos_liga)
            partidos_lista = [par for jornada in jornadas for par in jornada]
            vuelta = [(v, u) for (u, v) in partidos_lista]
            partidos_lista = partidos_lista + vuelta

        # Si el usuario pidió aleatorizar el orden de los partidos:
        if aleatorio:
            random.shuffle(partidos_lista)

        total_partidos = len(partidos_lista)
        if total_partidos == 0:
            return render(request, 'principal/prueba.html', {
                'ligas': ligas,
                'equipos': equipos,
                'error': 'No se generaron partidos para esta liga.'
            })

        # ---------- Asignación de fechas ----------
        # Distribuimos los partidos equitativamente a lo largo del periodo de la liga
        if dias_totales == 1:
            offsets = [0] * total_partidos
        else:
            offsets = []
            for i in range(total_partidos):
                offset = int(
                    round(i * (dias_totales - 1) / (total_partidos - 1)))
                offsets.append(offset)
        fechas_programadas = [fecha_inicio +
                              timedelta(days=o) for o in offsets]
        hora_fija = time(18, 0)

        # ---------- Creación de partidos (DB) ----------
        with transaction.atomic():
            for (equip_local, equip_visitante), fecha_partido in zip(partidos_lista, fechas_programadas):
                fecha_hora = datetime.combine(fecha_partido, hora_fija)
                partido = Partido.objects.create(
                    liga=liga,
                    equipo_local=equip_local,
                    equipo_visitante=equip_visitante,
                    fecha_hora=fecha_hora,
                    estado='pendiente',
                    administrador=request.user if request.user.is_authenticated else None
                )
                partidos_generados.append(partido)

    return render(request, 'principal/prueba.html', {
        'ligas': ligas,
        'equipos': equipos,
        'partidos': partidos_generados
    })


# Vistas para administrar partidos

@login_required
@staff_member_required
def administrar_partido(request, partido_id):
    partido = get_object_or_404(Partido, id=partido_id)

    if request.user != partido.administrador:
        return HttpResponseForbidden("No tienes permiso para administrar este partido")

    eventos = partido.eventos.select_related('jugador')

    return render(request, 'principal/administrar_partido.html', {
        'partido': partido,
        'eventos': eventos
    })


@staff_member_required
def iniciar_partido(request, partido_id):
    partido = get_object_or_404(Partido, id=partido_id)

    if request.user != partido.administrador:
        return HttpResponseForbidden()

    if partido.estado == 'pendiente':
        partido.estado = 'en_juego'
        partido.save()

    return redirect('administrar_partido', partido_id=partido.id)


@staff_member_required
def anotar_gol(request, partido_id, equipo):
    partido = get_object_or_404(Partido, id=partido_id)

    if partido.estado != 'en_juego':
        return redirect('administrar_partido', partido_id=partido.id)

    if equipo == 'local':
        partido.goles_local += 1
    elif equipo == 'visitante':
        partido.goles_visitante += 1

    partido.save()

    return redirect('administrar_partido', partido_id=partido.id)


from decimal import Decimal
from .services.elo import actualizar_elo
from .services.mlp_dataset import guardar_partido_historico

@staff_member_required
@transaction.atomic
def finalizar_partido(request, partido_id):
    partido = get_object_or_404(Partido, id=partido_id)

    if partido.estado == 'finalizado':
        return redirect('administrar_partido', partido_id=partido.id)

    partido.estado = 'finalizado'
    partido.save()

    partido.guardar_resultado()
    actualizar_elo(partido)
    guardar_partido_historico(partido)

    # 🔎 Resolver apuestas
    apuestas = Apuesta.objects.filter(
        partido=partido,
        estado='pendiente'
    )

    for apuesta in apuestas:
        if apuesta.es_ganadora():   # método del modelo
            ganancia = apuesta.calcular_ganancia()

            perfil = apuesta.usuario.perfil
            perfil.saldo += ganancia
            perfil.save()

            MovimientoSaldo.objects.create(
                usuario=apuesta.usuario,
                tipo='premio',
                monto=ganancia,
                descripcion=f"Apuesta ganada partido {partido.id}"
            )

            apuesta.estado = 'ganada'
        else:
            apuesta.estado = 'perdida'

        apuesta.save()

    return redirect('administrar_partido', partido_id=partido.id)


@staff_member_required
def mi_partido(request):
    partidos = (Partido.objects.filter(
            administrador=request.user,
            estado__in=['pendiente', 'en_juego'],
            fecha_hora__gt=timezone.now()
        )
        .order_by('fecha_hora')[:30]
    )
    return render(request, 'principal/mi_partido.html', {
        'partidos': partidos,
    })


@staff_member_required
def registrar_evento(request, partido_id):
    partido = get_object_or_404(Partido, id=partido_id)

    # Seguridad básica
    if request.user != partido.administrador:
        return redirect('administrar_partido', partido_id=partido.id)

    if partido.estado != 'en_juego':
        return redirect('administrar_partido', partido_id=partido.id)

    if request.method == "POST":
        jugador_id = request.POST.get("jugador")
        tipo_evento = request.POST.get("tipo_evento")
        minuto = request.POST.get("minuto")
        detalle = request.POST.get("detalle")

        jugador = get_object_or_404(Jugador, id=jugador_id)

        EventoPartido.objects.create(
            partido=partido,
            jugador=jugador,
            tipo_evento=tipo_evento,
            minuto=minuto,
            detalle=detalle
        )

    return redirect('administrar_partido', partido_id=partido.id)


@login_required
@receiver(post_save, sender=User)
def crear_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(usuario=instance)


from decimal import Decimal
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib import messages


@superuser_required
def recargar_saldo(request):

    usuarios = User.objects.all().order_by('username')

    if request.method == "POST":
        try:
            user_id = request.POST.get("usuario")
            monto = Decimal(request.POST.get("monto"))

            if not user_id or monto <= 0:
                raise ValueError

            usuario = User.objects.get(id=user_id)

            perfil = usuario.perfil
            perfil.saldo += monto
            perfil.save()

            MovimientoSaldo.objects.create(
                usuario=usuario,
                tipo='recarga',
                monto=monto,
                descripcion=f"Recarga administrativa por {request.user.username}"
            )

            messages.success(
                request,
                f"Saldo recargado correctamente a {usuario.username}"
            )
            return redirect("recargar_saldo")

        except:
            messages.error(request, "Datos inválidos")

    return render(request, "principal/recargar_saldo.html", {
        "usuarios": usuarios
    })



from .services.cuotas import abrir_apuestas
@login_required
@staff_member_required
def abrir_apuestas_partido(request, partido_id):
    partido = get_object_or_404(Partido, id=partido_id)

    if partido.estado != 'pendiente':
        return redirect('administrar_partido', partido_id=partido.id)

    abrir_apuestas(partido)
    return redirect('administrar_partido', partido_id=partido.id)
