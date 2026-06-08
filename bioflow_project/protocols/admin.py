from django.contrib import admin
from .models import Categoria, Protocolo

# Registrando as tabelas para elas aparecerem no painel do administrador
admin.site.register(Categoria)
admin.site.register(Protocolo)