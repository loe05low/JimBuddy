from django.contrib import admin
from .models import Rating


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """
    Admin pentru gestiunea rating-urilor și comentariilor
    """
    list_display = ('from_user', 'to_user', 'rating', 'sesiune', 'data', 'has_comment')
    list_filter = ('rating', 'data')
    search_fields = ('from_user__nume', 'to_user__nume', 'comentariu')
    readonly_fields = ('data',)

    fieldsets = (
        ('Participanți', {
            'fields': ('from_user', 'to_user', 'sesiune')
        }),
        ('Evaluare', {
            'fields': ('rating', 'comentariu')
        }),
        ('Metadata', {
            'fields': ('data',),
            'classes': ('collapse',)
        }),
    )

    def has_comment(self, obj):
        return bool(obj.comentariu)
    has_comment.boolean = True
    has_comment.short_description = 'Are comentariu'
