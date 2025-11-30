from rest_framework.routers import DefaultRouter
from .views import ProductoViewSet, CategoriaViewSet, InventarioMovimientoViewSet

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'inventario-movimientos', InventarioMovimientoViewSet)


urlpatterns = router.urls
