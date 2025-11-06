from django.contrib import admin
from .models import Sala


@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    """
    Admin pentru gestiunea sălilor de fitness
    Admin-ul poate adăuga/șterge/edita săli
    """
    list_display = ('nume', 'adresa', 'latitudine', 'longitudine', 'created_at')
    search_fields = ('nume', 'adresa')
    list_filter = ('created_at',)
    readonly_fields = ('id', 'created_at', 'updated_at')

    fieldsets = (
        ('Informații Sală', {
            'fields': ('nume', 'adresa')
        }),
        ('Coordonate Hartă', {
            'fields': ('latitudine', 'longitudine'),
            'description': 'Coordonatele GPS pentru afișare pe hartă (OpenStreetMap)'
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
