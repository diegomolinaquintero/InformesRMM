from django import forms
from .models import Respuesta

class RespuestaForm(forms.ModelForm):
    class Meta:
        model = Respuesta
        fields = '__all__'

    def __init__(self, *args, niveles_usuario=None, usuario_autenticado=None, **kwargs):
        super().__init__(*args, **kwargs)

        # Si tienes niveles disponibles, limita las opciones del campo 'nivel'
        if niveles_usuario:
            self.fields['nivel'].queryset = niveles_usuario

        # Si el usuario está autenticado, establece automáticamente el campo 'usuario'
        if usuario_autenticado:
            self.fields['usuario'].initial = usuario_autenticado
            self.fields['usuario'].widget.attrs['disabled'] = True

    # Puedes agregar widgets personalizados o validaciones si es necesario
