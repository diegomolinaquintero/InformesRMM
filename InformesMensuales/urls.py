from django.urls import path
from .views import InformacionProfesor

urlpatterns = [
    path('informacion-profesor/<str:cedula>/', InformacionProfesor.as_view(), name='informacion-profesor'),
    # Agrega otras URL según tus necesidades
]

