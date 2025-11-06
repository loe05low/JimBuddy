from django.contrib import admin
from .models import Achievement, UserAchievement


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['icon', 'name', 'category', 'required_count', 'xp_reward', 'rarity']
    list_filter = ['category', 'rarity']
    search_fields = ['name', 'description', 'key']
    readonly_fields = ['id', 'created_at']
    ordering = ['category', 'required_count']

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'description', 'icon', 'category')
        }),
        ('Criteria', {
            'fields': ('key', 'required_count')
        }),
        ('Rewards', {
            'fields': ('xp_reward', 'rarity')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ['user', 'achievement', 'progress', 'is_unlocked', 'unlocked_at']
    list_filter = ['achievement__category', 'unlocked_at']
    search_fields = ['user__nume', 'achievement__name']
    readonly_fields = ['id', 'unlocked_at']
    ordering = ['-unlocked_at']

    def is_unlocked(self, obj):
        return obj.is_unlocked
    is_unlocked.boolean = True
    is_unlocked.short_description = 'Unlocked'
