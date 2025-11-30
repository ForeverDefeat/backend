from rest_framework import serializers
from .models import Venta, DetalleVenta
from apps.inventario.models import Producto
from apps.usuarios.models import Usuario


# -----------------------------
# SERIALIZADOR SIMPLE DE PRODUCTO
# -----------------------------
class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ('id_producto', 'nombre')


# -----------------------------
# SERIALIZADOR SIMPLE DE USUARIO
# -----------------------------
class UsuarioSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id_usuario', 'nombre', 'email']



# -----------------------------
# SERIALIZADOR DE DETALLE DE VENTA
# -----------------------------
class DetalleVentaSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer(read_only=True)

    class Meta:
        model = DetalleVenta
        fields = ('id_detalle', 'cantidad', 'precio_unitario', 'venta', 'producto')



# -----------------------------
# SERIALIZADOR DE VENTA COMPLETA
# -----------------------------
class VentaSerializer(serializers.ModelSerializer):

    # Relación inversa: venta.detalleventa_set
    detalles = DetalleVentaSerializer(source='detalleventa_set', many=True, read_only=True)

    # Usuario que registró la venta
    usuario = UsuarioSimpleSerializer(read_only=True)

    class Meta:
        model = Venta
        fields = ['id_venta', 'fecha', 'total', 'usuario', 'detalles']



# -----------------------------
# SIMPLE PRODUCTO (OPCIONAL)
# -----------------------------
class ProductoSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id_producto', 'nombre']
