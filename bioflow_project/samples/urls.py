from django.urls import path
from . import views

app_name = 'samples'

urlpatterns = [
    path('', views.sample_list, name='sample_list'),
    path('new/', views.sample_create, name='sample_create'),
    path('<int:pk>/', views.sample_detail, name='sample_detail'),
    path('<int:pk>/edit/', views.sample_edit, name='sample_edit'),
    path('<int:pk>/status/', views.sample_update_status, name='sample_update_status'),
]
