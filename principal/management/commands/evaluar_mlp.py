from django.core.management.base import BaseCommand
from principal.services.mlp_evaluacion import evaluar_mlp


class Command(BaseCommand):
    help = "Evalúa métricas del modelo MLP"

    def handle(self, *args, **kwargs):

        res = evaluar_mlp()

        self.stdout.write(self.style.SUCCESS("\n=== MATRIZ DE CONFUSIÓN ==="))
        self.stdout.write(str(res["matriz"]))

        self.stdout.write(self.style.SUCCESS("\n=== RECALL POR CLASE ==="))
        self.stdout.write(str(res["recall"]))

        self.stdout.write(self.style.SUCCESS("\n=== LOG LOSS ==="))
        self.stdout.write(str(res["logloss"]))
