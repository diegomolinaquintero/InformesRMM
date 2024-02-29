from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.admin import RelatedOnlyFieldListFilter
from .models import Sexo, TipoDocumentoIdentidad, Instrumento, Rol, Usuario, Escuela, UsuarioNivel, Mes, Pregunta, Respuesta, InformeConsolidado, Ciclo, Nivel

# Personalizamos el modelo de usuario en el administrador
class UsuarioInline(admin.StackedInline):
    model = Usuario
    can_delete = False
    verbose_name_plural = 'Usuario'

# Extendemos el UserAdmin para incluir el modelo Usuario
class CustomUserAdmin(UserAdmin):
    inlines = (UsuarioInline,)

class NivelAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'get_ciclo_name')

    def get_ciclo_name(self, obj):
        return obj.ciclo.nombre if obj.ciclo else None

    get_ciclo_name.short_description = 'Ciclo'    

# Register UserAdmin with the model of usuario
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Nivel, NivelAdmin)

class EscuelaCicloFilter(RelatedOnlyFieldListFilter):
    def field_choices(self, field, request, model_admin):
        return super().field_choices(field, request, model_admin).filter(ciclos__isnull=False).distinct()

@admin.register(Sexo)
class SexoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(TipoDocumentoIdentidad)
class TipoDocumentoIdentidadAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(Instrumento)
class InstrumentoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'rol', 'sexo', 'tipo_documento_identidad', 'numero_documento_identidad', 'instrumento', 'niveles_display')
    list_filter = ('rol', 'sexo', 'tipo_documento_identidad', 'instrumento')
    search_fields = ('user__username', 'numero_documento_identidad')

    def niveles_display(self, obj):
        return ', '.join([str(usuario_nivel.nivel) for usuario_nivel in obj.niveles_asignados.all()])

@admin.register(Escuela)
class EscuelaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(UsuarioNivel)
class UsuarioNivelAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'nivel')
    list_filter = ('nivel', 'usuario')

@admin.register(Mes)
class MesAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ('texto', 'mes')
    list_filter = ('roles', 'mes')

@admin.register(Respuesta)
class RespuestaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'pregunta', 'ciclo', 'nivel', 'respuesta', 'fecha_respuesta', 'mes')
    list_filter = ('ciclo', 'nivel', 'mes', 'usuario')

@admin.register(InformeConsolidado)
class InformeConsolidadoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'ciclo', 'escuela', 'numero_informe')
    search_fields = ('usuario__user__username', 'numero_informe')

@admin.register(Ciclo)
class CicloAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'get_niveles')

    def get_niveles(self, obj):
        return ', '.join([nivel.nombre for nivel in obj.nivel_set.all()])

    get_niveles.short_description = 'Niveles Asociados'

