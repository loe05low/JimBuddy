from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'tip', 'titlu', 'citit', 'data_creare']
    list_filter = ['tip', 'citit', 'data_creare']
    search_fields = ['user__nume', 'titlu', 'mesaj']
    readonly_fields = ['id', 'data_creare', 'data_citire']
    ordering = ['-data_creare']
