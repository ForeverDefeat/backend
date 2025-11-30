from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import VentaViewSet, DetalleVentaViewSet, registrar_venta

router = DefaultRouter()
router.register(r'detalles', DetalleVentaViewSet)
router.register(r'ventas', VentaViewSet)

urlpatterns = [
    path("registrar-venta/", registrar_venta),

]

urlpatterns += router.urls
