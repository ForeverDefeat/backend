from rest_framework import serializers
from .models import Usuario, Rol

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    rol = RolSerializer(read_only=True)
    id_rol = serializers.PrimaryKeyRelatedField(queryset=Rol.objects.all(), source='rol', write_only=True)

    class Meta:
        model = Usuario
        fields = ['id_usuario', 'nombre', 'email', 'password', 'rol', 'id_rol', 'estado']
        extra_kwargs = {'password': {'write_only': True}}