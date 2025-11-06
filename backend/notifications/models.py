import uuid
from django.db import models
from users.models import UserProfile


class Notification(models.Model):
    """
    Notificări pentru utilizatori
    Tipuri: cerere_noua, cerere_acceptata, cerere_refuzata, sesiune_reminder, rating_nou
    """
    NOTIFICATION_TYPES = [
        ('cerere_noua', 'New Buddy Request'),
        ('cerere_acceptata', 'Request Accepted'),
        ('cerere_refuzata', 'Request Rejected'),
        ('sesiune_reminder', 'Session Reminder'),
        ('rating_nou', 'New Rating Received'),
        ('achievement_unlocked', 'Achievement Unlocked'),
        ('follow_nou', 'New Follower'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='notifications')
    tip = models.CharField(max_length=30, choices=NOTIFICATION_TYPES)
    titlu = models.CharField(max_length=200)
    mesaj = models.TextField()

    # Optional: link to related object
    link = models.CharField(max_length=200, blank=True, null=True, help_text="URL to navigate when clicked")

    # Metadata
    citit = models.BooleanField(default=False)
    data_creare = models.DateTimeField(auto_now_add=True)
    data_citire = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ['-data_creare']

    def __str__(self):
        return f"{self.user.nume} - {self.titlu} ({'Read' if self.citit else 'Unread'})"

    def mark_as_read(self):
        """Mark notification as read"""
        from django.utils import timezone
        if not self.citit:
            self.citit = True
            self.data_citire = timezone.now()
            self.save(update_fields=['citit', 'data_citire'])
