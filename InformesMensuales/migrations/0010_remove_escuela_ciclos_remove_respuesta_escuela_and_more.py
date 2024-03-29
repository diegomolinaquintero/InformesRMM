# Generated by Django 5.0.2 on 2024-02-29 15:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InformesMensuales', '0009_remove_ciclo_escuela_remove_nivel_ciclo_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='escuela',
            name='ciclos',
        ),
        migrations.RemoveField(
            model_name='respuesta',
            name='escuela',
        ),
        migrations.AddField(
            model_name='ciclo',
            name='escuela',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='ciclos', to='InformesMensuales.escuela'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usuario',
            name='niveles',
            field=models.ManyToManyField(related_name='usuarios', through='InformesMensuales.UsuarioNivel', to='InformesMensuales.nivel'),
        ),
        migrations.AddField(
            model_name='usuarionivel',
            name='ciclo',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='InformesMensuales.ciclo'),
            preserve_default=False,
        ),
    ]
