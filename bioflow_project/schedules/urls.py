from django.urls import path
from . import views

urlpatterns = [
    path(
        '',
        views.schedule_list,
        name='schedule_list'
    ),

    path(
        'create/',
        views.schedule_create,
        name='schedule_create'
    ),

    path(
        '<int:pk>/',
        views.schedule_detail,
        name='schedule_detail'
    ),

    path(
        '<int:pk>/delete/',
        views.schedule_delete,
        name='schedule_delete'
    ),
]
