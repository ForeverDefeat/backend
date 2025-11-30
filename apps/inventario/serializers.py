""" from rest_framework import serializers
from .models import Producto, Categoria, InventarioMovimiento

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)
    id_categoria = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all(), source='categoria', write_only=True)

    class Meta:
        model = Producto
        fields = ['id_producto', 'nombre', 'descripcion', 'precio_compra', 'precio_venta', 'stock', 'categoria', 'id_categoria', 'imagen_url', 'estado']

class InventarioMovimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventarioMovimiento
        fields = '__all__'
 """
 
from rest_framework import serializers
from .models import Producto, Categoria, InventarioMovimiento

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'


class ProductoSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)
    id_categoria = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(),
        source='categoria',
        write_only=True
    )
    
    # 👉 Nuevo campo solo lectura para mostrar el nombre de categoría en el frontend
    categoria_nombre = serializers.CharField(
        source='categoria.nombre',
        read_only=True
    )

    class Meta:
        model = Producto
        fields = [
            'id_producto', 
            'nombre', 
            'descripcion', 
            'precio_compra', 
            'precio_venta', 
            'stock',
            'stock_minimo', 
            'categoria', 
            'id_categoria', 
            'categoria_nombre',   
            'imagen_url', 
            'estado'
        ]


class InventarioMovimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventarioMovimiento
        fields = '__all__'
