from django.urls import path
from . import views

app_name = 'protocols'

urlpatterns = [
    path('', views.protocol_list, name='protocol_list'),
    path('new/', views.protocol_create, name='protocol_create'),
    path('<int:pk>/', views.protocol_detail, name='protocol_detail'),
    path('<int:pk>/edit/', views.protocol_edit, name='protocol_edit'),
]
