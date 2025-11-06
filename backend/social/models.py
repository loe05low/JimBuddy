import uuid
from django.db import models
from users.models import UserProfile


class Follow(models.Model):
    """
    Follow/Friend system
    follower = user who follows
    following = user being followed
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    follower = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='following'
    )
    following = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='followers'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Follow"
        verbose_name_plural = "Follows"
        ordering = ['-created_at']
        unique_together = ['follower', 'following']

    def __str__(self):
        return f"{self.follower.nume} follows {self.following.nume}"

    def save(self, *args, **kwargs):
        # Prevent self-follow
        if self.follower == self.following:
            raise ValueError("Users cannot follow themselves")
        super().save(*args, **kwargs)


class ActivityLog(models.Model):
    """
    Activity feed for social features
    Tracks: workouts completed, ratings given, achievements unlocked, etc.
    """
    ACTIVITY_TYPES = [
        ('workout_completed', 'Completed Workout'),
        ('rating_given', 'Gave Rating'),
        ('achievement_unlocked', 'Unlocked Achievement'),
        ('session_created', 'Created Session'),
        ('level_up', 'Leveled Up'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=30, choices=ACTIVITY_TYPES)
    description = models.TextField()

    # Optional references
    related_user = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='related_activities'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Activities"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.nume} - {self.get_activity_type_display()}"
