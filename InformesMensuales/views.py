from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profesor, ProfesorEscuela, CicloNiveles, EscuelaCiclos, Preguntas, ProfesorRoles
from rest_framework.permissions import AllowAny

class InformacionProfesor(APIView):
    permission_classes = [AllowAny] 
    def get(self, request, cedula, format=None):
        try:
            profesor = Profesor.objects.get(documento_identidad=cedula)
        except Profesor.DoesNotExist:
            return Response({"error": "Profesor no encontrado"}, status=404)

        profesor_escuelas = ProfesorEscuela.objects.filter(profesor=profesor)
        data = []

        for profesor_escuela in profesor_escuelas:
            escuela = profesor_escuela.escuela
            escuela_ciclos = EscuelaCiclos.objects.filter(escuela=escuela)
            ciclos_niveles = CicloNiveles.objects.filter(ciclo__in=escuela_ciclos.values('ciclo'))

            # ciclos_niveles = CicloNiveles.objects.filter(ciclo__in=EscuelaCiclos.objects.filter(escuela=escuela))
            
            escuela_info = {
                'escuela_nombre': escuela.nombre,
                'escuela_direccion': escuela.direccion,
                'ciclos_niveles': []
            }

            for ciclo_nivel in ciclos_niveles:
                ciclo_info = {
                    'ciclo_nombre': ciclo_nivel.ciclo.nombre,
                    'nivel_nombre': ciclo_nivel.nivel.nombre,
                    'preguntas': []
                }
                profesor_roles = ProfesorRoles.objects.filter(profesor=profesor)
                roles = profesor_roles.values('rol')
                preguntas = Preguntas.objects.filter(rol__in=roles)
                # preguntas = Preguntas.objects.filter(rol__in=ProfesorRoles.objects.filter(profesor=profesor))
                for pregunta in preguntas:
                    ciclo_info['preguntas'].append({
                        'pregunta': pregunta.pregunta,
                        'rol_nombre': pregunta.rol.nombre
                    })

                escuela_info['ciclos_niveles'].append(ciclo_info)

            data.append(escuela_info)

        return Response(data)
