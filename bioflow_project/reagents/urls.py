from django.urls import path
from . import views
app_name = 'reagents'
urlpatterns = [
    path('', views.reagent_list, name='reagent_list'),
    path('<int:pk>/', views.reagent_detail, name='reagent_detail'),
    path('new/', views.reagent_create, name='reagent_create'),
    path('<int:pk>/edit/', views.reagent_edit, name='reagent_edit'),
    path('<int:pk>/delete/', views.reagent_delete, name='reagent_delete'),
]
