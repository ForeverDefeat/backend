from django.db import models
from apps.usuarios.models import Usuario

# Create your models here.

class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'categorias'

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    stock_minimo = models.IntegerField(default=5)
    categoria = models.ForeignKey(
        Categoria, on_delete=models.CASCADE, db_column='id_categoria'
    )
    imagen_url = models.CharField(max_length=255, blank=True, null=True)
    estado = models.BooleanField(default=True)

    class Meta:
        db_table = 'productos'

    def __str__(self):
        return self.nombre


class InventarioMovimiento(models.Model):
    id_movimiento = models.AutoField(primary_key=True)
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, db_column='id_producto'
    )
    tipo = models.CharField(
        max_length=10,
        choices=[('entrada', 'Entrada'),
                 ('salida', 'Salida'),
                 ('ajuste', 'Ajuste')]
    )
    cantidad = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, db_column='id_usuario'
    )
    observacion = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'inventario_movimientos'

    def __str__(self):
        return f"{self.tipo} - {self.producto.nombre}"