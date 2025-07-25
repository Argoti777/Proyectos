# Generated by Django 5.0.14 on 2025-07-15 02:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Equipo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('ciudad', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'Equipos',
            },
        ),
        migrations.CreateModel(
            name='Liga',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('pais', models.CharField(max_length=100)),
                ('ciudad', models.CharField(max_length=100)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
            ],
            options={
                'db_table': 'Ligas',
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('correo', models.EmailField(max_length=100, unique=True)),
                ('numero', models.CharField(max_length=11, unique=True)),
                ('contraseña', models.CharField(max_length=255)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('rol', models.CharField(default='usuario', max_length=50)),
            ],
            options={
                'db_table': 'Usuarios',
            },
        ),
        migrations.CreateModel(
            name='Jugador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('edad', models.IntegerField()),
                ('posicion', models.CharField(max_length=50)),
                ('equipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jugadores', to='principal.equipo')),
            ],
            options={
                'db_table': 'Jugadores',
            },
        ),
        migrations.AddField(
            model_name='equipo',
            name='liga',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='equipos', to='principal.liga'),
        ),
        migrations.CreateModel(
            name='Partido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_hora', models.DateTimeField()),
                ('goles_local', models.IntegerField(default=0)),
                ('goles_visitante', models.IntegerField(default=0)),
                ('estado', models.CharField(max_length=50)),
                ('equipo_local', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partidos_locales', to='principal.equipo')),
                ('equipo_visitante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partidos_visitantes', to='principal.equipo')),
                ('liga', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='principal.liga')),
            ],
            options={
                'db_table': 'Partidos',
            },
        ),
        migrations.CreateModel(
            name='EventoPartido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_evento', models.CharField(max_length=50)),
                ('minuto', models.IntegerField()),
                ('detalle', models.TextField(blank=True, null=True)),
                ('jugador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eventos', to='principal.jugador')),
                ('partido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eventos', to='principal.partido')),
            ],
            options={
                'db_table': 'EventosPartidos',
            },
        ),
        migrations.AddField(
            model_name='liga',
            name='administrador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ligas', to='principal.usuario'),
        ),
    ]
