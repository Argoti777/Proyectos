import numpy as np
from principal.models import PartidoHistoricoMLP, EloEquipo
from principal.services.mlp_model import cargar_mlp
from principal.services.elo import probabilidades_partido


UMBRAL_MLP = 300


def probabilidades_mlp(partido):
    """
    Devuelve probabilidades usando MLP si hay datos suficientes,
    caso contrario usa ELO.
    """
    total = PartidoHistoricoMLP.objects.filter(liga=partido.liga).count()
    
    print("USANDO MLP") if total >= UMBRAL_MLP else print("USANDO ELO")
    # ---- Fallback a ELO ----
    if total < UMBRAL_MLP:
        return probabilidades_partido(partido)

    # ---- Cargar modelo ----
    model, scaler = cargar_mlp()

    elo_local = EloEquipo.objects.get(
        equipo=partido.equipo_local,
        liga=partido.liga
    )
    elo_visitante = EloEquipo.objects.get(
        equipo=partido.equipo_visitante,
        liga=partido.liga
    )

    X = np.array([[
        elo_local.rating,
        elo_visitante.rating,
        elo_local.rating - elo_visitante.rating,
        elo_local.partidos_jugados,
        elo_visitante.partidos_jugados
    ]])

    X_scaled = scaler.transform(X)
    probs = model.predict_proba(X_scaled)[0]

    return {
        "local": round(float(probs[0]), 3),
        "empate": round(float(probs[1]), 3),
        "visitante": round(float(probs[2]), 3),
    }
