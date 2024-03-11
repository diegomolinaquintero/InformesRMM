from django.urls import path
from .views import InformacionProfesor, RespuestaProfesorCreateView

urlpatterns = [
    path('informacion-profesor/<str:cedula>/', InformacionProfesor.as_view(), name='informacion-profesor'),
    # Agrega otras URL según tus necesidades
    path('respuesta_profesor/create/', RespuestaProfesorCreateView.as_view(), name='create_respuesta_profesor'),

]

