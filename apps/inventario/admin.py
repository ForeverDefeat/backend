from django.contrib import admin
from .models import Producto, Categoria, InventarioMovimiento

# Register your models here.
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(InventarioMovimiento)

