from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Profesor, ProfesorEscuela, CicloNiveles, EscuelaCiclos, Preguntas, ProfesorRoles
from rest_framework.permissions import AllowAny
from .models import RespuestaProfesor
from .serializers import RespuestaProfesorSerializer
from .models import RespuestaProfesor, Escuela, Ciclo, Nivel, Rol, Preguntas, Mes

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


class RespuestaProfesorCreateView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        data = request.data

        # Retrieve or create related objects
        escuela, created = Escuela.objects.get_or_create(nombre=data['escuela_nombre'])
        ciclo, created = Ciclo.objects.get_or_create(nombre=data['ciclo_nombre'])
        nivel, created = Nivel.objects.get_or_create(nombre=data['nivel_nombre'])
        rol, created = Rol.objects.get_or_create(nombre=data['rol_nombre'])
        pregunta, created = Preguntas.objects.get_or_create(pregunta=data['pregunta']['pregunta'], rol=rol)
        mes, created = Mes.objects.get_or_create(nombre=data['mes_nombre'])

        # Create RespuestaProfesor instance
        respuesta_profesor_data = {
            'escuela': escuela,
            'ciclo': ciclo,
            'nivel': nivel,
            'rol': rol,
            'pregunta': pregunta,
            'mes': mes,
            'respuesta': data['respuesta'],
        }

        serializer = RespuestaProfesorSerializer(data=respuesta_profesor_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)