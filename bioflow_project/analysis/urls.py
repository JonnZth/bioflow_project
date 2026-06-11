from django.urls import path
from . import views
app_name='analysis'
urlpatterns=[
    path('',views.analysis_list,name='analysis_list'),
    path('<int:pk>/',views.analysis_detail,name='analysis_detail'),
    path('new/',views.analysis_create,name='analysis_create'),
]
