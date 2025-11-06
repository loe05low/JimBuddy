import uuid
from django.db import models
from django.utils import timezone
from users.models import UserProfile
from workouts.models import Sesiune


class Conversation(models.Model):
    """
    Conversație de chat - poate fi privată (2 users) sau de grup (sesiune)
    """
    TYPE_CHOICES = [
        ('private', 'Private'),
        ('group', 'Group'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='private')

    # Pentru chat privat
    user1 = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='conversations_as_user1',
        blank=True,
        null=True
    )
    user2 = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='conversations_as_user2',
        blank=True,
        null=True
    )

    # Pentru chat de grup (sesiune)
    sesiune = models.OneToOneField(
        Sesiune,
        on_delete=models.CASCADE,
        related_name='conversation',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Conversație"
        verbose_name_plural = "Conversații"
        ordering = ['-updated_at']

    def __str__(self):
        if self.type == 'private':
            return f"Private: {self.user1.nume} & {self.user2.nume}"
        else:
            return f"Group: {self.sesiune.tip_antrenament}"


class Message(models.Model):
    """
    Mesaj în cadrul unei conversații
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField(help_text="Conținutul mesajului")
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Mesaj"
        verbose_name_plural = "Mesaje"
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender.nume}: {self.content[:50]}"
