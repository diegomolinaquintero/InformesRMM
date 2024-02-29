from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404, redirect
from .models import Pregunta, Respuesta, Nivel
from .forms import RespuestaForm



@login_required
def dashboard(request):
    usuario = request.user.usuario  # Suponiendo que el usuario está autenticado y tiene un perfil de Usuario
    niveles_usuario = usuario.niveles.all()  # Obtener los niveles asociados al usuario

    if request.method == 'POST':
        form = RespuestaForm(request.POST)
        if form.is_valid():
            # Guardar la respuesta asociada al usuario, pregunta, nivel, etc.
            respuesta = form.save(commit=False)
            respuesta.usuario = usuario
            respuesta.nivel = form.cleaned_data['nivel']  # Obtener el nivel desde el formulario
            respuesta.ciclo = respuesta.nivel.ciclo  # Suponiendo que necesitas el ciclo asociado al nivel
            respuesta.mes = form.cleaned_data['mes']
            respuesta.save()
            return redirect('página_de_destino')  # Redirige a la página que desees después de guardar la respuesta
    else:
        form = RespuestaForm(niveles_usuario=niveles_usuario)


    return render(request, 'InformesMensuales/dashboard.html',{'form': form})

def exit(request):
    logout(request)
    return redirect('dashboard')
