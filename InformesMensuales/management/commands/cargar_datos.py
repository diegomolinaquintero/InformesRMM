import pandas as pd
from django.contrib.auth.models import User as AuthUser
from django.core.management.base import BaseCommand
from InformesMensuales.models import Rol, Mes, Ciclo, Nivel, Escuela, Profesor, EscuelaCiclos, CicloNiveles, Preguntas
# Asegúrate de cambiar 'mi_app' por el nombre real de tu aplicación Django

class Command(BaseCommand):
    help = "Carga los datos de Excel a la base de datos."

    def cargar_mes(self):
        df = pd.read_excel('/home/siata/Downloads/SubirArchivosREMM-20240315T161734Z-001/SubirArchivosREMM/mes.xlsx')
        for _, row in df.iterrows():
            Mes.objects.get_or_create(nombre=row['nombre'])

    def cargar_rol(self):
        df = pd.read_excel('/home/siata/Downloads/SubirArchivosREMM-20240315T161734Z-001/SubirArchivosREMM/rol.xlsx')
        for _, row in df.iterrows():
            Rol.objects.get_or_create(nombre=row['nombre'], descripcion=row['descripcion'])

    def cargar_ciclo(self):
        df = pd.read_excel('/home/siata/Downloads/SubirArchivosREMM-20240315T161734Z-001/SubirArchivosREMM/ciclo.xlsx')
        for _, row in df.iterrows():
            Ciclo.objects.get_or_create(nombre=row['nombre'], descripcion=row['descripcion'])

    def cargar_nivel(self):
        df = pd.read_excel('/home/siata/Downloads/SubirArchivosREMM-20240315T161734Z-001/SubirArchivosREMM/nivel.xlsx')
        for _, row in df.iterrows():
            Nivel.objects.get_or_create(nombre=row['nombre'], descripcion=row['descripcion'])

    def cargar_escuela(self):
        df = pd.read_excel('/home/siata/Downloads/SubirArchivosREMM-20240315T161734Z-001/SubirArchivosREMM/Escuela.xlsx')
        for _, row in df.iterrows():
            Escuela.objects.get_or_create(nombre=row['nombre'], direccion=row['direccion'])

    def cargar_user(self):
        df = pd.read_excel('/home/siata/Downloads/SubirArchivosREMM-20240315T161734Z-001/SubirArchivosREMM/User.xlsx')
        for _, row in df.iterrows():
            username = row['Username']
            email = row['Email']
            password = str(row['Password'])  # Convierte explícitamente la contraseña a una cadena
            user, created = AuthUser.objects.get_or_create(username=username, email=email)
            if created:
                user.set_password(password)
                user.save()

    def cargar_profesor(self):
        df = pd.read_excel('/home/siata/Downloads/SubirArchivosREMM-20240315T161734Z-001/SubirArchivosREMM/profesor.xlsx')
        for _, row in df.iterrows():
            user = AuthUser.objects.get(username=row['user'])
            profesor, _ = Profesor.objects.get_or_create(
                user=user,
                documento_identidad=row['documento de identidad']
            )
            roles = row['rol'].split(';')  # Asume que los roles están separados por ';'
            for nombre_rol in roles:
                rol = Rol.objects.get(nombre=nombre_rol.strip())
                profesor.roles.add(rol)

    def cargar_escuela_ciclos(self):
        df = pd.read_excel('/home/siata/Downloads/SubirArchivosREMM-20240315T161734Z-001/SubirArchivosREMM/EscuelaCiclos.xlsx')
        for _, row in df.iterrows():
            # Aquí, asumimos que 'nombre_escuela' y 'nombre_ciclo' son los nombres de las columnas en tu Excel
            # que contienen los nombres de las escuelas y los ciclos, respectivamente.
            escuela_nombre = row['escuela']
            ciclo_nombre = row['ciclo']
            
            # Busca la escuela y el ciclo por nombre para obtener sus instancias
            escuela = Escuela.objects.get(nombre=escuela_nombre)
            ciclo = Ciclo.objects.get(nombre=ciclo_nombre)
            
            # Una vez que tienes las instancias, puedes crear o actualizar EscuelaCiclos
            # usando las instancias directamente, Django manejará los ID por ti
            EscuelaCiclos.objects.get_or_create(escuela=escuela, ciclo=ciclo)

    def cargar_ciclo_niveles(self):
        df = pd.read_excel('/home/siata/Downloads/SubirArchivosREMM-20240315T161734Z-001/SubirArchivosREMM/CicloNiveles.xlsx')
        for _, row in df.iterrows():
            nombre_ciclo = row['ciclo']
            nombre_nivel = row['nivel']

            ciclo = Ciclo.objects.get(nombre=nombre_ciclo)
            nivel = Nivel.objects.get(nombre=nombre_nivel)

            CicloNiveles.objects.get_or_create(ciclo=ciclo, nivel=nivel)

    def cargar_preguntas(self):
        df = pd.read_excel('/home/siata/Downloads/SubirArchivosREMM-20240315T161734Z-001/SubirArchivosREMM/Preguntas.xlsx')
        for _, row in df.iterrows():
            nombre_rol = row['rol']  # Asume que esta es la columna con el nombre del rol en tu Excel
            texto_pregunta = row['pregunta']  # Asume que esta es la columna con el texto de la pregunta
            
            # Busca el Rol por su nombre
            try:
                rol = Rol.objects.get(nombre=nombre_rol)
            except Rol.DoesNotExist:
                print(f"No se encontró el Rol con nombre {nombre_rol}")
                continue  # Salta esta iteración si no se encuentra el Rol
            
            # Crea o actualiza la pregunta
            pregunta, created = Preguntas.objects.get_or_create(
                pregunta=texto_pregunta,
                defaults={'rol': rol}
            )
            
            if created:
                print(f"Pregunta '{texto_pregunta}' creada con éxito.")
            else:
                print(f"Pregunta '{texto_pregunta}' ya existente, no se creó.")

    def handle(self, *args, **options):
        self.cargar_mes()
        self.cargar_rol()
        self.cargar_ciclo()
        self.cargar_nivel()
        self.cargar_escuela()
        self.cargar_user()
        self.cargar_profesor()
        self.cargar_escuela_ciclos()
        self.cargar_ciclo_niveles()
        self.cargar_preguntas()
        self.stdout.write(self.style.SUCCESS('Todos los datos han sido cargados exitosamente.'))
