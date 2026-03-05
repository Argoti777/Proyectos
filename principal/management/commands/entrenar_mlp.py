from django.core.management.base import BaseCommand
from principal.services.mlp_model import entrenar_mlp


class Command(BaseCommand):
    help = "Entrena el modelo MLP usando el histórico de partidos"

    def handle(self, *args, **options):
        try:
            info = entrenar_mlp()
            self.stdout.write(self.style.SUCCESS(
                f"MLP entrenada correctamente | "
                f"Muestras: {info['muestras']} | "
                f"Accuracy (train): {info['accuracy']:.2f}"
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(str(e)))
