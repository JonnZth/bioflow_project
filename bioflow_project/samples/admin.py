from django.contrib import admin
from .models import Sample, SampleTracking


class SampleTrackingInline(admin.TabularInline):
    model = SampleTracking
    extra = 0
    readonly_fields = ('timestamp', 'changed_by', 'status', 'notes')


@admin.register(Sample)
class SampleAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'sample_type', 'status', 'responsible', 'collection_date')
    list_filter = ('status', 'sample_type', 'storage_location')
    search_fields = ('code', 'name', 'origin')
    inlines = [SampleTrackingInline]


@admin.register(SampleTracking)
class SampleTrackingAdmin(admin.ModelAdmin):
    list_display = ('sample', 'status', 'changed_by', 'timestamp')
    list_filter = ('status',)
    readonly_fields = ('timestamp',)
