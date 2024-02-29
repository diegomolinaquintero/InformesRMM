# Generated by Django 5.0.2 on 2024-02-22 14:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InformesMensuales', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='groups',
            field=models.ManyToManyField(related_name='usuarios', to='auth.group'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='user_permissions',
            field=models.ManyToManyField(related_name='usuarios', to='auth.permission'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='rol',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuarios', to='InformesMensuales.rol'),
        ),
        migrations.AlterField(
            model_name='usuarioescuela',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='escuelas_asignadas', to='InformesMensuales.usuario'),
        ),
    ]