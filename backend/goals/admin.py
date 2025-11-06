from django.contrib import admin
from .models import Goal, UserGoal


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ['icon', 'name', 'goal_type', 'period', 'target_value', 'xp_reward', 'is_active']
    list_filter = ['goal_type', 'period', 'is_active']
    search_fields = ['name', 'description']
    readonly_fields = ['id', 'created_at']
    ordering = ['goal_type', 'target_value']

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'description', 'icon', 'goal_type', 'period')
        }),
        ('Targets & Rewards', {
            'fields': ('target_value', 'xp_reward', 'duration_days')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Metadata', {
            'fields': ('id', 'created_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserGoal)
class UserGoalAdmin(admin.ModelAdmin):
    list_display = ['user', 'goal', 'status', 'progress_display', 'deadline', 'completed_at']
    list_filter = ['status', 'goal__goal_type', 'created_at']
    search_fields = ['user__nume', 'goal__name']
    readonly_fields = ['id', 'progress_percentage', 'is_completed', 'is_expired', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

    def progress_display(self, obj):
        return f"{obj.current_value}/{obj.goal.target_value} ({obj.progress_percentage}%)"
    progress_display.short_description = 'Progress'

    fieldsets = (
        ('Goal Info', {
            'fields': ('user', 'goal', 'status')
        }),
        ('Progress', {
            'fields': ('current_value', 'progress_percentage', 'current_streak', 'last_streak_date')
        }),
        ('Dates', {
            'fields': ('start_date', 'deadline', 'completed_at')
        }),
        ('Computed Fields', {
            'fields': ('is_completed', 'is_expired'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
