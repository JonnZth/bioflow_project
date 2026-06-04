from django.contrib import admin
from .models import Schedule


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):

    list_display = (
        'equipment',
        'user',
        'start_datetime',
        'end_datetime',
        'status'
    )

    list_filter = (
        'status',
        'equipment',
        'start_datetime'
    )

    search_fields = (
        'equipment__name',
        'user__username',
        'purpose'
    )

    ordering = (
        'start_datetime',
    )
