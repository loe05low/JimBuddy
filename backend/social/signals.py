from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Follow, ActivityLog
from notifications.models import Notification


@receiver(post_save, sender=Follow)
def create_follow_notification(sender, instance, created, **kwargs):
    """
    Create notification when someone follows you
    """
    if created:
        Notification.objects.create(
            user=instance.following,  # User being followed
            tip='follow_nou',
            titlu='New Follower! 👥',
            mesaj=f'{instance.follower.nume} started following you',
            link=f'/profile'  # Link to profile or followers page
        )

        # Create activity log
        ActivityLog.objects.create(
            user=instance.follower,
            activity_type='session_created',  # Will add more types later
            description=f'{instance.follower.nume} started following {instance.following.nume}'
        )
