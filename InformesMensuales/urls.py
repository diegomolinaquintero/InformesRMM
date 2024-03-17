from django.urls import path
from .views import InformacionProfesor, RespuestaProfesorCreateView

urlpatterns = [
    path('informacion-profesor/<str:cedula>/<str:mes>/', InformacionProfesor.as_view(), name='informacion-profesor'),
    # Agrega otras URL según tus necesidades
    path('respuesta_profesor/<str:cedula>/<str:mes>/', RespuestaProfesorCreateView.as_view(), name='respuesta_profesor'),

]

