from django.contrib import admin
from .models import Sesiune, Cerere, SessionParticipant


class CerereInline(admin.TabularInline):
    """
    Afișează cererile direct în pagina sesiunii
    """
    model = Cerere
    extra = 0
    readonly_fields = ('applicant', 'data_creare', 'data_raspuns')
    can_delete = False


class ParticipantInline(admin.TabularInline):
    """
    Afișează participanții direct în pagina sesiunii
    """
    model = SessionParticipant
    extra = 0
    readonly_fields = ('user', 'joined_at')
    can_delete = True


@admin.register(Sesiune)
class SesiuneAdmin(admin.ModelAdmin):
    """
    Admin pentru gestiunea sesiunilor de antrenament
    """
    list_display = ('user', 'sala', 'tip_antrenament', 'city', 'interval_orar', 'private', 'max_participants', 'status', 'data_creare')
    list_filter = ('status', 'tip_antrenament', 'private', 'city', 'data_creare')
    search_fields = ('user__nume', 'sala__nume', 'tip_antrenament', 'city')
    readonly_fields = ('id', 'data_creare')
    inlines = [ParticipantInline, CerereInline]

    fieldsets = (
        ('Informații Sesiune', {
            'fields': ('user', 'sala', 'tip_antrenament', 'interval_orar', 'data_sesiune', 'city', 'descriere', 'image')
        }),
        ('Settings', {
            'fields': ('private', 'max_participants')
        }),
        ('Status & Timeline', {
            'fields': ('status', 'data_creare', 'data_expirare')
        }),
        ('Metadata', {
            'fields': ('id',),
            'classes': ('collapse',)
        }),
    )

    actions = ['arhiveaza_sesiuni']

    def arhiveaza_sesiuni(self, request, queryset):
        """
        Action pentru arhivarea manuală a sesiunilor selectate
        """
        count = queryset.update(status='arhivat')
        self.message_user(request, f'{count} sesiuni au fost arhivate.')
    arhiveaza_sesiuni.short_description = "Arhivează sesiunile selectate"


@admin.register(Cerere)
class CerereAdmin(admin.ModelAdmin):
    """
    Admin pentru gestiunea cererilor de gym buddy
    """
    list_display = ('applicant', 'sesiune', 'status', 'data_creare', 'data_raspuns')
    list_filter = ('status', 'data_creare')
    search_fields = ('applicant__nume', 'sesiune__user__nume')
    readonly_fields = ('id', 'data_creare', 'data_raspuns')

    fieldsets = (
        ('Informații Cerere', {
            'fields': ('sesiune', 'applicant', 'status')
        }),
        ('Timeline', {
            'fields': ('data_creare', 'data_raspuns')
        }),
        ('Metadata', {
            'fields': ('id',),
            'classes': ('collapse',)
        }),
    )


@admin.register(SessionParticipant)
class SessionParticipantAdmin(admin.ModelAdmin):
    """
    Admin pentru participanți la sesiuni
    """
    list_display = ('user', 'sesiune', 'joined_at')
    list_filter = ('joined_at',)
    search_fields = ('user__nume', 'sesiune__tip_antrenament')
    readonly_fields = ('id', 'joined_at')
