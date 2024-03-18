# importarasignaciones.py
# /home/siata/Downloads/SubirArchivosREMM-20240315T161734Z-001/SubirArchivosREMM/relaciones_consolidadas_final_completo_ajuste.xlsx
from django.core.management.base import BaseCommand
from InformesMensuales.models import Asignacion, ProfesorEscuela, EscuelaCiclos, CicloNiveles, Profesor
import pandas as pd

class Command(BaseCommand):
    help = 'Importa las asignaciones desde un archivo Excel predeterminado'

    archivo_excel = '/home/siata/Downloads/SubirArchivosREMM-20240315T161734Z-001/SubirArchivosREMM/relaciones_consolidadas_final_completo_ajuste.xlsx'

    def handle(self, *args, **kwargs):
        try:
            df = pd.read_excel(self.archivo_excel)
            self.stdout.write(self.style.SUCCESS(f'Archivo {self.archivo_excel} cargado correctamente'))
        except FileNotFoundError:
            raise CommandError(f'Archivo {self.archivo_excel} no encontrado')
        except Exception as e:
            raise CommandError(f'Error al leer el archivo {self.archivo_excel}: {e}')

        for index, row in df.iterrows():
            if pd.isnull(row['Ciclo_Nombre']):
                self.stdout.write(self.style.WARNING(f'Fila {index} omitida: falta nombre de ciclo'))
                continue

            niveles = [nivel.strip() for nivel in row['Niveles'].split(',') if nivel.strip()]

            try:
                profesor = Profesor.objects.get(documento_identidad=row['Documento de Identidad'])
            except Profesor.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Profesor no encontrado para el documento {row["Documento de Identidad"]}'))
                continue

            for nivel in niveles:
                try:
                    escuela_ciclo = EscuelaCiclos.objects.filter(escuela__nombre=row['Escuela'], ciclo__nombre=row['Ciclo_Nombre']).first()
                    if not escuela_ciclo:
                        self.stdout.write(self.style.WARNING(f'EscuelaCiclos no encontrada para {row["Escuela"]} y ciclo {row["Ciclo_Nombre"]}'))
                        continue

                    ciclo_niveles = CicloNiveles.objects.get(ciclo__nombre=row['Ciclo_Nombre'], nivel__nombre=nivel)

                    profesor_escuela, created = ProfesorEscuela.objects.get_or_create(
                        profesor=profesor, 
                        escuela=escuela_ciclo.escuela
                    )

                    asignacion = Asignacion(
                        profesor_escuela=profesor_escuela,
                        escuela_ciclos=escuela_ciclo,
                        ciclo_niveles=ciclo_niveles
                    )
                    asignacion.save()
                    self.stdout.write(self.style.SUCCESS(f'Asignación creada correctamente para documento {row["Documento de Identidad"]} - {nivel}'))

                except CicloNiveles.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'CicloNiveles no encontrado para {row["Ciclo_Nombre"]} y {nivel}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error al procesar la fila {index} y nivel {nivel}: {e}'))