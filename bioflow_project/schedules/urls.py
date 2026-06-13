from django.urls import path
from . import views
app_name='schedules'
urlpatterns=[
    path('',views.schedule_list,name='schedule_list'),
    path('new/',views.schedule_create,name='schedule_create'),
    path('<int:pk>/cancel/',views.schedule_cancel,name='schedule_cancel'),
]
