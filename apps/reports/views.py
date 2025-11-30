from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, F
from datetime import datetime
from apps.ventas.models import Venta, DetalleVenta
from apps.inventario.models import InventarioMovimiento, Producto
from .serializers import (
    VentasReportSerializer,
    UtilidadesReportSerializer,
    StockCriticoSerializer
)



class SalesSummaryView(APIView):
    """
    Devuelve ventas totales, total de dinero generado y cantidad de ventas.
    """

    def get(self, request):
        total_ventas = Venta.objects.count()
        total_monto = Venta.objects.aggregate(total=Sum("total"))["total"] or 0

        return Response({
            "total_ventas": total_ventas,
            "total_monto": float(total_monto),
        }, status=status.HTTP_200_OK)


class TopProductsView(APIView):
    """
    Devuelve los productos más vendidos por cantidad.
    """

    def get(self, request):
        top = (
            DetalleVenta.objects
            .values(nombre=F("producto__nombre"))
            .annotate(cantidad_total=Sum("cantidad"))
            .order_by("-cantidad_total")[:5]
        )

        return Response(top, status=status.HTTP_200_OK)


class InventoryMovementsView(APIView):
    """
    Devuelve el resumen de entradas, salidas y ajustes.
    """

    def get(self, request):
        movimientos = (
            InventarioMovimiento.objects
            .values("tipo")
            .annotate(total=Sum("cantidad"))
        )

        return Response(movimientos, status=status.HTTP_200_OK)

# ------------------------------------------------------------------
# 1) REPORTE DE VENTAS POR DÍA O MES
# ------------------------------------------------------------------
@api_view(['GET'])
def ventas_report(request):
    tipo = request.GET.get("tipo", "dia")  # "dia" o "mes"
    
    if tipo == "dia":
        fecha = request.GET.get("fecha")
        if not fecha:
            return Response({"error": "Debe enviar ?fecha=YYYY-MM-DD"}, status=400)

        try:
            fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
        except:
            return Response({"error": "Formato incorrecto. Use YYYY-MM-DD"}, status=400)

        ventas = Venta.objects.filter(fecha=fecha_obj)
        total_ingresos = ventas.aggregate(total=Sum('total'))['total'] or 0

        data = {
            "periodo": str(fecha_obj),
            "cantidad_ventas": ventas.count(),
            "total_ingresos": float(total_ingresos)
        }

    else:  # tipo == "mes"
        anio = request.GET.get("anio")
        mes = request.GET.get("mes")

        if not anio or not mes:
            return Response({"error": "Debe enviar ?anio=YYYY&mes=MM"}, status=400)

        ventas = Venta.objects.filter(
            fecha__year=anio,
            fecha__month=mes
        )

        total_ingresos = ventas.aggregate(total=Sum('total'))['total'] or 0

        data = {
            "periodo": f"{anio}-{mes}",
            "cantidad_ventas": ventas.count(),
            "total_ingresos": float(total_ingresos)
        }

    serializer = VentasReportSerializer(data)
    return Response(serializer.data)


# ------------------------------------------------------------------
# 2) REPORTE DE UTILIDADES (Ingresos - Costos)
# ------------------------------------------------------------------
@api_view(['GET'])
def utilidades_report(request):

    fecha = request.GET.get("fecha")
    anio = request.GET.get("anio")
    mes = request.GET.get("mes")

    if fecha:
        # FILTRO POR DÍA
        try:
            fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
        except:
            return Response({"error": "Formato incorrecto. Use YYYY-MM-DD"}, status=400)

        detalles = DetalleVenta.objects.filter(venta__fecha=fecha_obj)
        periodo = str(fecha_obj)

    elif anio and mes:
        # FILTRO POR MES
        detalles = DetalleVenta.objects.filter(
            venta__fecha__year=anio,
            venta__fecha__month=mes
        )
        periodo = f"{anio}-{mes}"

    else:
        return Response({"error": "Debe enviar ?fecha= o ?anio=&mes="}, status=400)

    ingresos = detalles.aggregate(total=Sum(F('cantidad') * F('precio_unitario')))['total'] or 0
    costos = detalles.aggregate(total=Sum(F('cantidad') * F('producto__costo')))['total'] or 0

    data = {
        "periodo": periodo,
        "ingresos": float(ingresos),
        "costos": float(costos),
        "utilidad": float(ingresos - costos)
    }

    serializer = UtilidadesReportSerializer(data)
    return Response(serializer.data)


# ------------------------------------------------------------------
# 3) REPORTE DE STOCK CRÍTICO
# ------------------------------------------------------------------
@api_view(['GET'])
def stock_critico_report(request):
    productos = Producto.objects.filter(stock__lt=F('stock_minimo'))

    data = [
        {
            "id": p.id_producto,
            "nombre": p.nombre,
            "stock": p.stock,
            "stock_minimo": p.stock_minimo,
            "categoria": p.categoria.nombre
        }
        for p in productos
    ]

    return Response(data)

@api_view(['GET'])
def ventas_detalladas_report(request):

    fecha_desde = request.GET.get("from")
    fecha_hasta = request.GET.get("to")
    categoria = request.GET.get("category")
    producto = request.GET.get("product")
    empleado = request.GET.get("employee")

    detalles = DetalleVenta.objects.select_related("producto", "venta")

    # FILTRO POR FECHA DESDE
    if fecha_desde:
        detalles = detalles.filter(venta__fecha__date__gte=fecha_desde)

    # FILTRO POR FECHA HASTA
    if fecha_hasta:
        detalles = detalles.filter(venta__fecha__date__lte=fecha_hasta)

    # FILTRO POR CATEGORÍA
    if categoria:
        detalles = detalles.filter(producto__categoria__id_categoria=categoria)

    # FILTRO POR PRODUCTO
    if producto:
        detalles = detalles.filter(producto__nombre__icontains=producto)

    # FILTRO POR EMPLEADO
    if empleado:
        detalles = detalles.filter(venta__usuario__nombre__icontains=empleado)

    # ORDENAR
    detalles = detalles.order_by("-venta__fecha")

    data = [
        {
            "id_venta": d.venta.id_venta,
            "fecha": d.venta.fecha,
            "producto": d.producto.nombre,
            "cantidad": d.cantidad,
            "precio_unitario": float(d.precio_unitario),
            "total": float(d.cantidad * d.precio_unitario),
        }
        for d in detalles
    ]

    return Response({"ventas": data}, status=200)
