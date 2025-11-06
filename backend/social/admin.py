from django.contrib import admin
from .models import Follow, ActivityLog


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following', 'created_at']
    list_filter = ['created_at']
    search_fields = ['follower__nume', 'following__nume']
    readonly_fields = ['id', 'created_at']
    ordering = ['-created_at']


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'description', 'created_at']
    list_filter = ['activity_type', 'created_at']
    search_fields = ['user__nume', 'description']
    readonly_fields = ['id', 'created_at']
    ordering = ['-created_at']
