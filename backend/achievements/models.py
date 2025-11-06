import uuid
from django.db import models
from users.models import UserProfile


class Achievement(models.Model):
    """
    Achievement template - defines what achievements exist
    Examples: First Workout, 10 Workouts, Social Butterfly, etc.
    """
    CATEGORY_CHOICES = [
        ('workout', 'Workout'),
        ('social', 'Social'),
        ('exploration', 'Exploration'),
        ('special', 'Special'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, help_text="Achievement name")
    description = models.TextField(help_text="What user needs to do to unlock this")
    icon = models.CharField(max_length=50, default='🏆', help_text="Emoji or icon identifier")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='workout')

    # Criteria for unlocking
    key = models.CharField(max_length=50, unique=True, help_text="Unique identifier for code (e.g., 'first_workout')")
    required_count = models.IntegerField(default=1, help_text="How many times action needs to happen")

    # Points and rarity
    xp_reward = models.IntegerField(default=10, help_text="XP points awarded")
    rarity = models.CharField(max_length=20, choices=[
        ('common', 'Common'),
        ('rare', 'Rare'),
        ('epic', 'Epic'),
        ('legendary', 'Legendary'),
    ], default='common')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Achievement"
        verbose_name_plural = "Achievements"
        ordering = ['category', 'required_count']

    def __str__(self):
        return f"{self.icon} {self.name}"


class UserAchievement(models.Model):
    """
    Junction table - tracks which achievements each user has unlocked
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name='unlocked_by')
    unlocked_at = models.DateTimeField(auto_now_add=True)

    # Progress tracking
    progress = models.IntegerField(default=0, help_text="Current progress towards achievement")

    class Meta:
        verbose_name = "User Achievement"
        verbose_name_plural = "User Achievements"
        unique_together = ['user', 'achievement']  # User can only unlock each achievement once
        ordering = ['-unlocked_at']

    def __str__(self):
        return f"{self.user.nume} - {self.achievement.name}"

    @property
    def is_unlocked(self):
        """Check if achievement is fully unlocked"""
        return self.progress >= self.achievement.required_count
