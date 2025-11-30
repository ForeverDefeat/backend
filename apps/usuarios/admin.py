from django.contrib import admin
from .models import Usuario, Rol  # Solo las clases que realmente están en usuarios/models.py

admin.site.register(Rol)
admin.site.register(Usuario)