from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profesor, RespuestaProfesor

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ProfesorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profesor
        fields = ['id', 'user', 'documento_identidad', 'roles']
        
from rest_framework import serializers

class RespuestaProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = RespuestaProfesor
        fields = '__all__'