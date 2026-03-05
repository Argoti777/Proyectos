from django.core.management.base import BaseCommand
from django.utils import timezone

from principal.models import Partido
from principal.services.simulador import simular_resultado
from principal.services.elo import actualizar_elo
from principal.services.mlp_dataset import guardar_partido_historico


class Command(BaseCommand):
    help = "Simula partidos finalizados para generar histórico MLP"

    def add_arguments(self, parser):
        parser.add_argument(
            '--cantidad',
            type=int,
            default=300,
            help='Cantidad de partidos a simular'
        )

    def handle(self, *args, **options):
        cantidad = options['cantidad']
        partidos = Partido.objects.filter(estado='pendiente')[:cantidad]

        total = 0

        for partido in partidos:
            goles_local, goles_visitante = simular_resultado(partido)

            partido.goles_local = goles_local
            partido.goles_visitante = goles_visitante
            partido.estado = 'finalizado'
            partido.fecha_hora = timezone.now()
            partido.save()

            partido.guardar_resultado()
            actualizar_elo(partido)
            guardar_partido_historico(partido)

            total += 1

        self.stdout.write(self.style.SUCCESS(
            f"{total} partidos simulados correctamente"
        ))
