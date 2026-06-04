from django.urls import path
from . import views
app_name='experiments'
urlpatterns=[
    path('',views.experiment_list,name='experiment_list'),
    path('<int:pk>/',views.experiment_detail,name='experiment_detail'),
    path('new/',views.experiment_create,name='experiment_create'),
    path('<int:pk>/edit/',views.experiment_edit,name='experiment_edit'),
]
