from rest_framework import viewsets
from .models import Producto, Categoria, InventarioMovimiento
from .serializers import ProductoSerializer, CategoriaSerializer, InventarioMovimientoSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.utils.stack import Stack

# Crear una pila global para la sesión (temporal)
historial_acciones = Stack()


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


class InventarioMovimientoViewSet(viewsets.ModelViewSet):
    queryset = InventarioMovimiento.objects.all()
    serializer_class = InventarioMovimientoSerializer


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    @action(detail=False, methods=['post'])
    def agregar_con_historial(self, request):
        nombre = request.data.get('nombre')
        stock = request.data.get('stock', 0)
        precio_compra = request.data.get('precio_compra')
        precio_venta = request.data.get('precio_venta')
        id_categoria = request.data.get('id_categoria')

        try:
            categoria = Categoria.objects.get(id_categoria=id_categoria)
        except Categoria.DoesNotExist:
            return Response({"error": "Categoría no encontrada"}, status=400)
        
        producto = Producto.objects.create(
            nombre=nombre,
            stock=stock,
            precio_compra=precio_compra,
            precio_venta=precio_venta,
            categoria=categoria
        )

        # Guardar acción en la pila
        historial_acciones.push({
            "accion": "agregar_producto",
            "producto_id": producto.id_producto
        })

        return Response({"mensaje": "Producto agregado y registrado en historial"})

    # Endpoint extra para deshacer última acción
    @action(detail=False, methods=['post'])
    def deshacer_ultima_accion(self, request):
        accion = historial_acciones.pop()
        if accion and accion["accion"] == "agregar_producto":
                Producto.objects.filter(id_producto=accion["producto_id"]).delete()
                return Response({"mensaje": "Última acción deshecha"})
        return Response({"mensaje": "No hay acciones para deshacer"})
