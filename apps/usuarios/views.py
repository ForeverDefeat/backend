from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from .models import Usuario, Rol
from .serializers import UsuarioSerializer, RolSerializer

class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

@api_view(['POST'])
def login_view(request):
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return Response({"error": "Email y password requeridos"}, status=400)

    try:
        user = Usuario.objects.get(email=email, estado=True)
    except Usuario.DoesNotExist:
        return Response({"error": "Credenciales inválidas"}, status=400)

    # Tus contraseñas NO están encriptadas → comparación directa
    if user.password != password:
        return Response({"error": "Credenciales incorrectas"}, status=400)

    return Response({
        "id_usuario": user.id_usuario,
        "nombre": user.nombre,
        "email": user.email,
        "rol": user.rol.nombre,
        "id_rol": user.rol.id_rol,
    })