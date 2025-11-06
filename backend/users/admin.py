from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, BlockedUser


class UserProfileInline(admin.StackedInline):
    """
    Inline pentru a edita profilul direct din pagina User
    """
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'


class UserAdmin(BaseUserAdmin):
    """
    Extinde Django User Admin pentru a include profilul
    """
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_rating', 'get_nr_antrenamente')

    def get_rating(self, obj):
        return f"{obj.profile.rating}★" if hasattr(obj, 'profile') else '-'
    get_rating.short_description = 'Rating'

    def get_nr_antrenamente(self, obj):
        return obj.profile.nr_antrenamente if hasattr(obj, 'profile') else 0
    get_nr_antrenamente.short_description = 'Antrenamente'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin pentru gestiunea directă a profilurilor
    """
    list_display = ('nume', 'city', 'grad', 'rating', 'nr_antrenamente', 'current_streak', 'user', 'created_at')
    list_filter = ('grad', 'rating', 'city')
    search_fields = ('nume', 'user__username', 'user__email', 'city')
    readonly_fields = ('created_at', 'updated_at', 'nr_antrenamente', 'rating', 'current_streak', 'last_workout_date')

    fieldsets = (
        ('Informații Utilizator', {
            'fields': ('user', 'nume', 'avatar', 'bio', 'city', 'phone')
        }),
        ('Statistici', {
            'fields': ('rating', 'nr_antrenamente', 'grad', 'current_streak', 'last_workout_date')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(BlockedUser)
class BlockedUserAdmin(admin.ModelAdmin):
    """
    Admin pentru utilizatori blocați
    """
    list_display = ('blocker', 'blocked', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('blocker__nume', 'blocked__nume')
    readonly_fields = ('created_at',)


# Re-înregistrează UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
