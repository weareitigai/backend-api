from django.contrib import admin
from .models import Destination, Language, TourType, Timezone


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'state', 'country', 'is_active']
    list_filter = ['country', 'state', 'is_active']
    search_fields = ['name', 'city', 'state', 'country']


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'code']


@admin.register(TourType)
class TourTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name']


@admin.register(Timezone)
class TimezoneAdmin(admin.ModelAdmin):
    list_display = ['name', 'offset', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']
