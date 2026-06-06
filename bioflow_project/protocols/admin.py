from django.contrib import admin
from .models import Protocol, ProtocolHistory


class ProtocolHistoryInline(admin.TabularInline):
    model = ProtocolHistory
    extra = 0
    readonly_fields = ('changed_at', 'changed_by')


@admin.register(Protocol)
class ProtocolAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'version', 'author', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('title',)
    inlines = [ProtocolHistoryInline]


@admin.register(ProtocolHistory)
class ProtocolHistoryAdmin(admin.ModelAdmin):
    list_display = ('protocol', 'version', 'changed_by', 'changed_at')
    readonly_fields = ('changed_at',)
