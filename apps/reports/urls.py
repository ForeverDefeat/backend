from django.urls import path
from .views import ventas_detalladas_report, SalesSummaryView, TopProductsView, InventoryMovementsView, ventas_report, utilidades_report, stock_critico_report

urlpatterns = [
    path("sales-summary/", SalesSummaryView.as_view(), name="sales-summary"),
    path("top-products/", TopProductsView.as_view(), name="top-products"),
    path("inventory-movements/", InventoryMovementsView.as_view(),
         name="inventory-movements"),
    path('ventas/', ventas_report, name='ventas_report'),
    path('utilidades/', utilidades_report, name='utilidades_report'),
    path('stock-critico/', stock_critico_report, name='stock_critico_report'),
    path("ventas/detalles/", ventas_detalladas_report, name="ventas_detalladas_report"),
]
