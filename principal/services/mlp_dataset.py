from principal.models import PartidoHistoricoMLP, EloEquipo


def guardar_partido_historico(partido):
    if PartidoHistoricoMLP.objects.filter(partido=partido).exists():
        return
    elo_local = EloEquipo.objects.get(
        equipo=partido.equipo_local,
        liga=partido.liga
    )
    elo_visitante = EloEquipo.objects.get(
        equipo=partido.equipo_visitante,
        liga=partido.liga
    )

    # Resultado
    if partido.goles_local > partido.goles_visitante:
        resultado = 0
    elif partido.goles_local < partido.goles_visitante:
        resultado = 2
    else:
        resultado = 1

    PartidoHistoricoMLP.objects.create(
        partido=partido,   # 👈 ESTO FALTA
        liga=partido.liga,
        elo_local=elo_local.rating,
        elo_visitante=elo_visitante.rating,
        diff_elo=elo_local.rating - elo_visitante.rating,
        partidos_local=elo_local.partidos_jugados,
        partidos_visitante=elo_visitante.partidos_jugados,
        resultado=resultado
    )
