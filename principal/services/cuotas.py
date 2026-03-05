from principal.models import Cuota
from principal.services.elo import probabilidades_partido
from principal.services.mlp_inferencia import probabilidades_mlp


def abrir_apuestas(partido):
    if Cuota.objects.filter(partido=partido).exists():
        return

    probs = probabilidades_mlp(partido)

    Cuota.objects.create(
        partido=partido,
        local=round(1 / probs['local'], 2),
        empate=round(1 / probs['empate'], 2),
        visitante=round(1 / probs['visitante'], 2),
        activa=True
    )




def crear_cuotas_para_partido(partido):
    """
    Crea cuotas para un partido si no existen
    """
    if Cuota.objects.filter(partido=partido).exists():
        return

    probs = probabilidades_partido(partido)

    Cuota.objects.create(
        partido=partido,
        local=round(1 / probs['local'], 2),
        empate=round(1 / probs['empate'], 2),
        visitante=round(1 / probs['visitante'], 2),
    )