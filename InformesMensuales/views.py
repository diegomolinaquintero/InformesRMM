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

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Profesor, Mes, Asignacion, ProfesorRoles, Preguntas, RespuestaProfesor, Escuela, Ciclo, Nivel

class InformacionProfesor(APIView):
    permission_classes = [AllowAny]

    def get(self, request, cedula, mes, format=None):
        profesor = get_object_or_404(Profesor, documento_identidad=cedula)
        mes_objeto = get_object_or_404(Mes, nombre=mes)

        data = {
            'persona_id': profesor.id,
            'persona_cedula': profesor.documento_identidad,
            'escuelas': []
        }

        asignaciones = Asignacion.objects.filter(
            profesor_escuela__profesor=profesor
        ).values(
            'profesor_escuela__escuela', 
            'ciclo_niveles__ciclo', 
            'ciclo_niveles__nivel'
        ).distinct()

        # Obtener los IDs de las escuelas para el profesor
        escuelas_ids = set([a['profesor_escuela__escuela'] for a in asignaciones])

        for escuela_id in escuelas_ids:
            escuela = Escuela.objects.get(id=escuela_id)
            escuela_info = {
                'escuela_id': escuela.id,
                'escuela_nombre': escuela.nombre,
                'escuela_direccion': escuela.direccion,
                'ciclos_niveles': []
            }

            # Filtrar los ciclos y niveles para esta escuela
            ciclos_niveles_ids = [(a['ciclo_niveles__ciclo'], a['ciclo_niveles__nivel']) for a in asignaciones if a['profesor_escuela__escuela'] == escuela_id]

            for ciclo_id, nivel_id in set(ciclos_niveles_ids):
                ciclo = Ciclo.objects.get(id=ciclo_id)
                nivel = Nivel.objects.get(id=nivel_id)
                ciclo_nivel_info = {
                    'ciclo_id': ciclo.id,
                    'ciclo_nombre': ciclo.nombre,
                    'nivel_id': nivel.id,
                    'nivel_nombre': nivel.nombre,
                    'preguntas': []
                }

                preguntas = Preguntas.objects.filter(rol__profesorroles__profesor=profesor).distinct()
                for pregunta in preguntas:
                    respuesta = RespuestaProfesor.objects.filter(
                        profesor=profesor,
                        pregunta=pregunta,
                        nivel=nivel,
                        ciclo=ciclo,
                        escuela=escuela,
                        mes=mes_objeto
                    ).first()

                    ciclo_nivel_info['preguntas'].append({
                        'pregunta_id': pregunta.id,
                        'pregunta': pregunta.pregunta,
                        'rol_id': pregunta.rol.id,
                        'rol_nombre': pregunta.rol.nombre,
                        'respuesta': respuesta.respuesta if respuesta else ""
                    })

                escuela_info['ciclos_niveles'].append(ciclo_nivel_info)

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