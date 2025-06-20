from django.db import models
from django.utils import timezone
# Create your models here.

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(max_length=100, unique=True)
    numero = models.CharField(max_length=11, unique=True)
    contraseña = models.CharField(max_length=255)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    rol = models.CharField(max_length=50, default='usuario')

    class Meta:
        db_table = "Usuarios"  # Esto hará que la tabla se llame "Usuarios" en la base de datos

    def __str__(self):
        return self.nombre