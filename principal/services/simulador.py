import random
from principal.services.elo import probabilidades_partido


def simular_resultado(partido):
    """
    Simula el resultado de un partido usando probabilidades ELO
    """
    probs = probabilidades_partido(partido)

    r = random.random()

    if r < probs['local']:
        # gana local
        return random.randint(1, 3), random.randint(0, 1)
    elif r < probs['local'] + probs['empate']:
        # empate
        g = random.randint(0, 2)
        return g, g
    else:
        # gana visitante
        return random.randint(0, 1), random.randint(1, 3)
