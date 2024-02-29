from django.contrib.auth.models import User, Group
from django.db import models


class Sexo(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class TipoDocumentoIdentidad(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Instrumento(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Rol(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, related_name='usuarios')
    sexo = models.ForeignKey(Sexo, on_delete=models.SET_NULL, null=True, blank=True)
    tipo_documento_identidad = models.ForeignKey(TipoDocumentoIdentidad, on_delete=models.SET_NULL, null=True, blank=True)
    numero_documento_identidad = models.CharField(max_length=20, unique=True, null=True, blank=True)
    instrumento = models.ForeignKey(Instrumento, on_delete=models.SET_NULL, null=True, blank=True)
    niveles = models.ManyToManyField('Nivel', through='UsuarioNivel', related_name='usuarios')

    groups = models.ManyToManyField(Group, related_name='usuarios_groups')

    def __str__(self):
        return f"{self.user} - {self.rol}"

class Escuela(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Ciclo(models.Model):
    nombre = models.CharField(max_length=50)
    escuela = models.ForeignKey(Escuela, on_delete=models.CASCADE, related_name='ciclos')
    

    def __str__(self):
        return f"{self.nombre} - {self.escuela}"

class Nivel(models.Model):
    nombre = models.CharField(max_length=50)
    ciclo = models.ForeignKey(Ciclo, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class UsuarioNivel(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='niveles_asignados')
    nivel = models.ForeignKey(Nivel, on_delete=models.CASCADE)


    def save(self, *args, **kwargs):
        self.ciclo = self.nivel.ciclo
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.usuario.user.username} - {self.nivel} - {self.ciclo}"

class Mes(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

class Pregunta(models.Model):
    texto = models.TextField()
    roles = models.ManyToManyField(Rol, related_name='preguntas')
    mes = models.ForeignKey(Mes, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.texto} - {self.mes}"

class Respuesta(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    ciclo = models.ForeignKey(Ciclo, on_delete=models.CASCADE)
    nivel = models.ForeignKey(Nivel, on_delete=models.CASCADE)
    respuesta = models.TextField()
    fecha_respuesta = models.DateTimeField(auto_now_add=True)
    mes = models.ForeignKey(Mes, on_delete=models.CASCADE)

class InformeConsolidado(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nivel = models.ForeignKey(Nivel, on_delete=models.CASCADE)
    ciclo = models.ForeignKey(Ciclo, on_delete=models.CASCADE)
    escuela = models.ForeignKey(Escuela, on_delete=models.CASCADE)
    numero_informe = models.CharField(max_length=20, unique=True)
    consolidado = models.TextField()

    def save(self, *args, **kwargs):
        self.numero_informe = f"{self.usuario.user.username}_{self.nivel.nombre}_{self.ciclo.nombre}_{self.escuela.nombre}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.numero_informe
    
    class Meta:
        unique_together = ['usuario', 'nivel', 'ciclo', 'escuela']
