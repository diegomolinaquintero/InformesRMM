from django.contrib.auth.models import User
from django.db import models

class Profesor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    documento_identidad = models.CharField(max_length=20)
    roles = models.ManyToManyField('Rol', through='ProfesorRoles')

    def __str__(self):
        return f"{self.user.username} - {self.documento_identidad}"

class Escuela(models.Model):
    nombre = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nombre} - {self.direccion}"

class Ciclo(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()

    def __str__(self):
        return f"{self.nombre} - {self.descripcion}"

class Nivel(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()

    def __str__(self):
        return f"{self.nombre} - {self.descripcion}"

class Rol(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()

    def __str__(self):
        return f"{self.nombre} - {self.descripcion}"

class ProfesorEscuela(models.Model):
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    escuela = models.ForeignKey(Escuela, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.profesor.user.username} - {self.escuela.nombre}"

class EscuelaCiclos(models.Model):
    escuela = models.ForeignKey(Escuela, on_delete=models.CASCADE)
    ciclo = models.ForeignKey(Ciclo, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.escuela.nombre} - {self.ciclo.nombre}"

class CicloNiveles(models.Model):
    ciclo = models.ForeignKey(Ciclo, on_delete=models.CASCADE)
    nivel = models.ForeignKey(Nivel, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.ciclo.nombre} - {self.nivel.nombre}"

class Asignacion(models.Model):
    profesor_escuela = models.ForeignKey(ProfesorEscuela, on_delete=models.CASCADE)
    escuela_ciclos = models.ForeignKey(EscuelaCiclos, on_delete=models.CASCADE)
    ciclo_niveles = models.ForeignKey(CicloNiveles, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.profesor_escuela.profesor.user.username} - {self.escuela_ciclos.escuela.nombre} - {self.ciclo_niveles.ciclo.nombre}"

class ProfesorRoles(models.Model):
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.profesor.user.username} - {self.rol.nombre}"
    
from django.db import models

class Preguntas(models.Model):
    pregunta = models.CharField(max_length=500)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.pregunta} - {self.rol.nombre}"
    
class Mes(models.Model):
    nombre = models.CharField(max_length=500)
    

    def __str__(self):
        return self.nombre
    
class RespuestaProfesor(models.Model):
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    nivel = models.ForeignKey(Nivel, on_delete=models.CASCADE)
    ciclo = models.ForeignKey(Ciclo, on_delete=models.CASCADE)
    escuela = models.ForeignKey(Escuela, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Preguntas, on_delete=models.CASCADE)
    mes = models.ForeignKey(Mes, on_delete=models.CASCADE)

    respuesta = models.TextField()

    def __str__(self):
        return f"{self.profesor.user.username} - {self.escuela.nombre} - {self.ciclo.nombre} - {self.nivel.nombre} - {self.rol.nombre} - {self.pregunta.pregunta} - {self.mes.nombre}"
