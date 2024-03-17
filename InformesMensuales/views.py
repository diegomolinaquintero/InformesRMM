from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Profesor, ProfesorEscuela, CicloNiveles, EscuelaCiclos, Preguntas, ProfesorRoles
from rest_framework.permissions import AllowAny
from .models import RespuestaProfesor
from .serializers import RespuestaProfesorSerializer
from .models import RespuestaProfesor, Escuela, Ciclo, Nivel, Rol, Preguntas, Mes, Asignacion
from django.db import transaction

class InformacionProfesor(APIView):
    permission_classes = [AllowAny]

    def get(self, request, cedula, mes, format=None):
        profesor = get_object_or_404(Profesor, documento_identidad=cedula)
        mes_objeto = get_object_or_404(Mes, nombre=mes)  # Asegura que el mes existe

        data = {
            'persona_id': profesor.id,
            'persona_cedula': profesor.documento_identidad,
            'escuelas': []
        }

        asignaciones = Asignacion.objects.filter(profesor_escuela__profesor=profesor)

        for asignacion in asignaciones:
            escuela = asignacion.profesor_escuela.escuela
            ciclo_nivel = asignacion.ciclo_niveles
            ciclo = ciclo_nivel.ciclo
            nivel = ciclo_nivel.nivel

            escuela_info = {
                'escuela_id': escuela.id,
                'escuela_nombre': escuela.nombre,
                'escuela_direccion': escuela.direccion,
                'ciclos_niveles': [{
                    'ciclo_id': ciclo.id,
                    'ciclo_nombre': ciclo.nombre,
                    'nivel_id': nivel.id,
                    'nivel_nombre': nivel.nombre,
                    'preguntas': []
                }]
            }

            profesor_roles = ProfesorRoles.objects.filter(profesor=profesor).select_related('rol')
            for profesor_rol in profesor_roles:
                preguntas = Preguntas.objects.filter(rol=profesor_rol.rol)

                for pregunta in preguntas:
                    respuesta = RespuestaProfesor.objects.filter(
                        profesor=profesor,
                        pregunta=pregunta,
                        nivel=nivel,
                        ciclo=ciclo,
                        escuela=escuela,
                        mes=mes_objeto  # Asegura que la respuesta corresponde al mes específico
                    ).first()

                    escuela_info['ciclos_niveles'][0]['preguntas'].append({
                        'pregunta_id': pregunta.id,
                        'pregunta': pregunta.pregunta,
                        'rol_id': profesor_rol.rol.id,
                        'rol_nombre': profesor_rol.rol.nombre,
                        'respuesta': respuesta.respuesta if respuesta else ""
                    })

            data['escuelas'].append(escuela_info)

        return Response(data)


class RespuestaProfesorCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, cedula, mes, *args, **kwargs):
        data = request.data
        profesor = get_object_or_404(Profesor, documento_identidad=cedula)
        mes_objeto = get_object_or_404(Mes, nombre=mes)  # Asegura que el mes existe

        # Asegúrate de que "respuestas" y "escuelas" existen y son diccionarios
        respuestas = data.get("respuestas", {})
        escuelas = respuestas.get("escuelas", {})

        for id_escuela, ciclos in escuelas.items():
            escuela = get_object_or_404(Escuela, id=id_escuela)
            for id_ciclo, niveles in ciclos.items():
                ciclo = get_object_or_404(Ciclo, id=id_ciclo)
                for id_nivel, preguntas in niveles.items():
                    nivel = get_object_or_404(Nivel, id=id_nivel)
                    for id_pregunta, respuesta_texto in preguntas.items():
                        pregunta = get_object_or_404(Preguntas, id=id_pregunta)
                        # Suponiendo que "idRol" es parte de la estructura (necesitas ajustarlo si no lo es)
                        id_rol = pregunta.rol_id  # O cómo determines el rol basado en la pregunta
                        rol = get_object_or_404(Rol, id=id_rol)

                        # Ahora puedes crear o actualizar la respuesta del profesor correctamente
                        respuesta_profesor, created = RespuestaProfesor.objects.update_or_create(
                            profesor=profesor,
                            escuela=escuela,
                            ciclo=ciclo,
                            nivel=nivel,
                            pregunta=pregunta,
                            mes=mes_objeto,
                            rol=rol,
                            defaults={'respuesta': respuesta_texto}
                        )

        return Response({"success": "Respuestas actualizadas correctamente."}, status=status.HTTP_200_OK)