from math import pow
from principal.models import EloEquipo


K_FACTOR = 30  # valor estándar, suficiente para ligas barriales


def obtener_elo(equipo, liga):
    elo, _ = EloEquipo.objects.get_or_create(
        equipo=equipo,
        liga=liga,
        defaults={'rating': 1200}
    )
    return elo


def expectativa(rating_a, rating_b):
    """
    Probabilidad esperada de que A gane frente a B
    """
    return 1 / (1 + pow(10, (rating_b - rating_a) / 400))


def actualizar_elo(partido):
    """
    Actualiza el ELO de ambos equipos cuando el partido finaliza
    """
    elo_local = obtener_elo(partido.equipo_local, partido.liga)
    elo_visitante = obtener_elo(partido.equipo_visitante, partido.liga)

    # Resultado real
    if partido.goles_local > partido.goles_visitante:
        resultado_local = 1
        resultado_visitante = 0
    elif partido.goles_local < partido.goles_visitante:
        resultado_local = 0
        resultado_visitante = 1
    else:
        resultado_local = 0.5
        resultado_visitante = 0.5

    # Expectativas
    exp_local = expectativa(elo_local.rating, elo_visitante.rating)
    exp_visitante = expectativa(elo_visitante.rating, elo_local.rating)

    # Actualización
    elo_local.rating += K_FACTOR * (resultado_local - exp_local)
    elo_visitante.rating += K_FACTOR * (resultado_visitante - exp_visitante)

    elo_local.partidos_jugados += 1
    elo_visitante.partidos_jugados += 1

    elo_local.save()
    elo_visitante.save()

def probabilidades_partido(partido):
    """
    Devuelve probabilidades (local, empate, visitante)
    basadas en ELO
    """
    elo_local = obtener_elo(partido.equipo_local, partido.liga)
    elo_visitante = obtener_elo(partido.equipo_visitante, partido.liga)

    exp_local = expectativa(elo_local.rating, elo_visitante.rating)
    exp_visitante = expectativa(elo_visitante.rating, elo_local.rating)

    diff = abs(elo_local.rating - elo_visitante.rating)

    # Probabilidad de empate ajustada por diferencia de ELO
    prob_empate = max(0.15, 0.30 - diff / 1000)

    resto = 1 - prob_empate

    prob_local = resto * exp_local
    prob_visitante = resto * exp_visitante

    return {
        'local': round(prob_local, 3),
        'empate': round(prob_empate, 3),
        'visitante': round(prob_visitante, 3)
    }
