from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_protocolos, name='listar_protocolos'),
    path('novo/', views.cadastrar_protocolo, name='cadastrar_protocolo'),
    path('editar/<int:pk>/', views.editar_protocolo, name='editar_protocolo'),
]