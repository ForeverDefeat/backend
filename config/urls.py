from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from apps.usuarios.views import UsuarioViewSet
from apps.inventario.views import CategoriaViewSet, ProductoViewSet, InventarioMovimientoViewSet
from apps.clientes.views import ClienteViewSet
from apps.ventas.views import VentaViewSet, DetalleVentaViewSet, DetalleVentaListView, registrar_venta

router = routers.DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'inventario', InventarioMovimientoViewSet)
router.register(r'ventas', VentaViewSet)
router.register(r'detalles-venta', DetalleVentaViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    # 💥 Endpoints personalizados DEBEN IR ANTES
    path('api/ventas/registrar/', registrar_venta, name='registrar_venta'),
    path('api/ventas/detalles/', DetalleVentaListView.as_view(), name="detalles_ventas"),

    # Reportes
    path('api/reports/', include('apps.reports.urls')),

    # Usuarios
    path('api/', include('apps.usuarios.urls')),

    # 💥 El router SIEMPRE al final
    path('api/', include(router.urls)),
]
