from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


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
    list_display = ('nume', 'grad', 'rating', 'nr_antrenamente', 'user', 'created_at')
    list_filter = ('grad', 'rating')
    search_fields = ('nume', 'user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at', 'nr_antrenamente', 'rating')

    fieldsets = (
        ('Informații Utilizator', {
            'fields': ('user', 'nume', 'poza')
        }),
        ('Statistici', {
            'fields': ('rating', 'nr_antrenamente', 'grad')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# Re-înregistrează UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
