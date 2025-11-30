from rest_framework import serializers

class VentasReportSerializer(serializers.Serializer):
    periodo = serializers.CharField()
    cantidad_ventas = serializers.IntegerField()
    total_ingresos = serializers.FloatField()

class UtilidadesReportSerializer(serializers.Serializer):
    periodo = serializers.CharField()
    ingresos = serializers.FloatField()
    costos = serializers.FloatField()
    utilidad = serializers.FloatField()

class StockCriticoSerializer(serializers.Serializer):
    producto = serializers.CharField()
    stock_actual = serializers.IntegerField()
    stock_minimo = serializers.IntegerField()

class VentaDetalleReporteSerializer(serializers.Serializer):
    id_venta = serializers.IntegerField()
    fecha = serializers.DateTimeField()
    producto = serializers.CharField()
    cantidad = serializers.IntegerField()
    precio_unitario = serializers.FloatField()
    total = serializers.FloatField()
