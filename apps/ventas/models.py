from django.db import models
from apps.usuarios.models import Usuario
from apps.inventario.models import Producto

# Create your models here.


class Venta(models.Model):
    id_venta = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, db_column='id_usuario'
    )

    class Meta:
        db_table = 'ventas'

    def __str__(self):
        return f"Venta #{self.id_venta}"


class DetalleVenta(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    venta = models.ForeignKey(
        Venta, on_delete=models.CASCADE, db_column='id_venta'
    )
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, db_column='id_producto'
    )
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'detalle_ventas'

    def __str__(self):
        return f"Detalle #{self.id_detalle} - {self.producto.nombre}"
