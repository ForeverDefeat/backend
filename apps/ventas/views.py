from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import transaction

from rest_framework import generics
from .models import Venta, DetalleVenta
from .serializers import VentaSerializer, DetalleVentaSerializer

from apps.inventario.models import Producto

from apps.utils.queue import Queue

# Cola global temporal para pedidos
cola_pedidos = Queue()


class DetalleVentaViewSet(viewsets.ModelViewSet):
    queryset = DetalleVenta.objects.all()
    serializer_class = DetalleVentaSerializer


class DetalleVentaListView(generics.ListAPIView):
    queryset = DetalleVenta.objects.all()
    serializer_class = DetalleVentaSerializer


class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer

    # Endpoints adicionales para manejar la cola de pedidos
    @action(detail=False, methods=['post'])
    def agregar_pedido(self, request):
        cliente_id = request.data.get('cliente_id')
        productos = request.data.get('productos', [])

        # Guardar pedido en la cola temporal
        pedido = {"cliente_id": cliente_id, "productos": productos}
        cola_pedidos.enqueue(pedido)

        return Response({"mensaje": "Pedido agregado a la cola", "cola_size": cola_pedidos.size()})

    # Endpoint para procesar el siguiente pedido en la cola
    @action(detail=False, methods=['post'])
    def procesar_pedido(self, request):
        pedido = cola_pedidos.dequeue()
        if pedido:
            # Aquí se podría guardar en la base de datos usando ORM
            nueva_venta = Venta.objects.create(cliente_id=pedido["cliente_id"])
            for prod_id in pedido["productos"]:
                DetalleVenta.objects.create(
                    venta=nueva_venta, producto_id=prod_id, cantidad=1)

            return Response({"mensaje": "Pedido procesado", "venta_id": nueva_venta.id})
        return Response({"mensaje": "No hay pedidos en la cola"})

    # Endpoint para ver el estado actual de la cola
    @action(detail=False, methods=['get'], url_path='ver-cola')
    def ver_cola(self, request):
        return Response({"cola": cola_pedidos.ver_cola()})


@api_view(['POST'])
@transaction.atomic
def registrar_venta(request):
    usuario_id = request.data.get("usuario_id")
    items = request.data.get("items", [])

    if not usuario_id:
        return Response({"error": "usuario_id es requerido"}, status=400)

    if not items:
        return Response({"error": "items no puede estar vacío"}, status=400)

    # Crear venta
    venta = Venta.objects.create(
        usuario_id=usuario_id,
        total=0
    )

    total_final = 0

    for item in items:
        prod_id = int(item.get("id_producto"))
        cantidad = int(item.get("cantidad"))
        precio_unitario = float(item.get("precio_venta"))

        # Obtener producto
        try:
            producto = Producto.objects.get(id_producto=prod_id)
        except Producto.DoesNotExist:
            transaction.set_rollback(True)
            return Response({"error": f"Producto {prod_id} no existe"}, status=400)

        # Validar stock
        if producto.stock < cantidad:
            transaction.set_rollback(True)
            return Response(
                {"error": f"Stock insuficiente para {producto.nombre}. Stock actual: {producto.stock}"},
                status=400
            )

        # Crear detalle
        DetalleVenta.objects.create(
            venta=venta,
            producto=producto,
            cantidad=cantidad,
            precio_unitario=precio_unitario
        )

        # Restar stock
        producto.stock -= cantidad
        producto.save()

        # Sumar total
        total_final += precio_unitario * cantidad

    # Actualizar total final
    venta.total = total_final
    venta.save()

    serializer = VentaSerializer(venta)
    return Response(serializer.data, status=201)
