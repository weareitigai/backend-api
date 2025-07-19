from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Destination, Language, TourType, Timezone


@admin.register(Destination)
class DestinationAdmin(ImportExportModelAdmin):
    list_display = ['name', 'city', 'state', 'country', 'is_active', 'created_at']
    list_filter = ['country', 'state', 'is_active', 'created_at']
    search_fields = ['name', 'city', 'state', 'country']
    ordering = ['name']
    list_per_page = 25
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']


@admin.register(Language)
class LanguageAdmin(ImportExportModelAdmin):
    list_display = ['name', 'code', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'code']
    ordering = ['name']
    list_per_page = 25


@admin.register(TourType)
class TourTypeAdmin(ImportExportModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name']
    ordering = ['name']
    list_per_page = 25
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']


@admin.register(Timezone)
class TimezoneAdmin(ImportExportModelAdmin):
    list_display = ['name', 'offset', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']
    ordering = ['name']
    list_per_page = 25
