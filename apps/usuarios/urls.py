from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, RolViewSet, login_view

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'roles', RolViewSet)

urlpatterns = [
    path("login/", login_view, name="login"),
]

urlpatterns += router.urls
