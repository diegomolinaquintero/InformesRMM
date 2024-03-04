from django.contrib import admin
from .models import Profesor, Escuela, Ciclo, Nivel, Rol, ProfesorEscuela, EscuelaCiclos, CicloNiveles, Asignacion, ProfesorRoles, Preguntas, Mes, RespuestaProfesor

@admin.register(Profesor)
class ProfesorAdmin(admin.ModelAdmin):
    list_display = ('user', 'documento_identidad')
    search_fields = ('user__username', 'documento_identidad')

@admin.register(Escuela)
class EscuelaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion')
    search_fields = ('nombre', 'direccion')

@admin.register(Ciclo)
class CicloAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre', 'descripcion')

@admin.register(Nivel)
class NivelAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre', 'descripcion')

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre', 'descripcion')

@admin.register(ProfesorEscuela)
class ProfesorEscuelaAdmin(admin.ModelAdmin):
    list_display = ('profesor', 'escuela')
    search_fields = ('profesor__user__username', 'escuela__nombre')

@admin.register(EscuelaCiclos)
class EscuelaCiclosAdmin(admin.ModelAdmin):
    list_display = ('escuela', 'ciclo')
    search_fields = ('escuela__nombre', 'ciclo__nombre')

@admin.register(CicloNiveles)
class CicloNivelesAdmin(admin.ModelAdmin):
    list_display = ('ciclo', 'nivel')
    search_fields = ('ciclo__nombre', 'nivel__nombre')

@admin.register(Asignacion)
class AsignacionAdmin(admin.ModelAdmin):
    list_display = ('profesor_escuela', 'escuela_ciclos', 'ciclo_niveles')
    search_fields = ('profesor_escuela__profesor__user__username', 'escuela_ciclos__escuela__nombre', 'ciclo_niveles__ciclo__nombre')

@admin.register(ProfesorRoles)
class ProfesorRolesAdmin(admin.ModelAdmin):
    list_display = ('profesor', 'rol')
    search_fields = ('profesor__user__username', 'rol__nombre')

@admin.register(Preguntas)
class PreguntasAdmin(admin.ModelAdmin):
    list_display = ('pregunta', 'rol')
    search_fields = ('pregunta', 'rol__nombre')

@admin.register(Mes)
class MesAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(RespuestaProfesor)
class RespuestaProfesorAdmin(admin.ModelAdmin):
    list_display = ('profesor', 'escuela', 'ciclo', 'nivel', 'rol', 'pregunta', 'mes', 'respuesta')
    search_fields = ('profesor__user__username', 'escuela__nombre', 'ciclo__nombre', 'nivel__nombre', 'rol__nombre', 'pregunta__pregunta', 'mes__nombre')
