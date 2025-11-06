import uuid
from django.db import models
from django.utils import timezone
from datetime import timedelta
from users.models import UserProfile


class Goal(models.Model):
    """
    Goal template - defines available goal types
    Examples: Complete 3 workouts this week, 5-day streak, etc.
    """
    GOAL_TYPE_CHOICES = [
        ('weekly_workouts', 'Weekly Workouts'),
        ('workout_streak', 'Workout Streak'),
        ('new_gyms', 'Visit New Gyms'),
        ('social', 'Social Engagement'),
        ('custom', 'Custom Goal'),
    ]

    PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('custom', 'Custom Period'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, help_text="Goal name")
    description = models.TextField(help_text="Goal description")
    goal_type = models.CharField(max_length=30, choices=GOAL_TYPE_CHOICES)
    period = models.CharField(max_length=20, choices=PERIOD_CHOICES, default='weekly')

    # Target metrics
    target_value = models.IntegerField(help_text="Target number to achieve (e.g., 3 workouts)")
    icon = models.CharField(max_length=50, default='🎯', help_text="Emoji or icon identifier")
    xp_reward = models.IntegerField(default=20, help_text="XP awarded on completion")

    # For custom period goals
    duration_days = models.IntegerField(default=7, help_text="Duration in days for custom periods")

    is_active = models.BooleanField(default=True, help_text="Is this goal template active?")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Goal Template"
        verbose_name_plural = "Goal Templates"
        ordering = ['goal_type', 'target_value']

    def __str__(self):
        return f"{self.icon} {self.name}"


class UserGoal(models.Model):
    """
    User's active goal with progress tracking
    """
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('abandoned', 'Abandoned'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='goals')
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='user_goals')

    # Progress tracking
    current_value = models.IntegerField(default=0, help_text="Current progress")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    # Time tracking
    start_date = models.DateTimeField(default=timezone.now)
    deadline = models.DateTimeField(help_text="Goal deadline")
    completed_at = models.DateTimeField(null=True, blank=True)

    # Streak tracking (for workout_streak type goals)
    current_streak = models.IntegerField(default=0, help_text="Current streak count")
    last_streak_date = models.DateField(null=True, blank=True, help_text="Last day streak was maintained")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User Goal"
        verbose_name_plural = "User Goals"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.nume} - {self.goal.name} ({self.status})"

    def save(self, *args, **kwargs):
        """Auto-set deadline based on goal period if not set"""
        if not self.deadline:
            if self.goal.period == 'daily':
                self.deadline = timezone.now() + timedelta(days=1)
            elif self.goal.period == 'weekly':
                self.deadline = timezone.now() + timedelta(weeks=1)
            elif self.goal.period == 'monthly':
                self.deadline = timezone.now() + timedelta(days=30)
            else:
                self.deadline = timezone.now() + timedelta(days=self.goal.duration_days)
        super().save(*args, **kwargs)

    @property
    def progress_percentage(self):
        """Calculate progress as percentage"""
        if self.goal.target_value == 0:
            return 0
        return min(100, int((self.current_value / self.goal.target_value) * 100))

    @property
    def is_completed(self):
        """Check if goal is completed"""
        return self.current_value >= self.goal.target_value and self.status == 'active'

    @property
    def is_expired(self):
        """Check if goal deadline has passed"""
        return timezone.now() > self.deadline and self.status == 'active'

    def complete(self):
        """Mark goal as completed"""
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save(update_fields=['status', 'completed_at'])

    def fail(self):
        """Mark goal as failed (deadline passed without completion)"""
        self.status = 'failed'
        self.save(update_fields=['status'])

    def abandon(self):
        """User abandoned the goal"""
        self.status = 'abandoned'
        self.save(update_fields=['status'])

    def increment_progress(self, amount=1):
        """Increment progress and check for completion"""
        self.current_value += amount
        self.save(update_fields=['current_value'])

        if self.is_completed:
            self.complete()
            return True
        return False

    def update_streak(self):
        """Update workout streak (for streak-type goals)"""
        from django.utils import timezone
        today = timezone.now().date()

        if self.last_streak_date is None:
            # First streak day
            self.current_streak = 1
            self.last_streak_date = today
        elif self.last_streak_date == today:
            # Already logged today
            pass
        elif self.last_streak_date == today - timedelta(days=1):
            # Consecutive day
            self.current_streak += 1
            self.last_streak_date = today
        else:
            # Streak broken
            self.current_streak = 1
            self.last_streak_date = today

        self.current_value = self.current_streak
        self.save()

        if self.is_completed:
            self.complete()
            return True
        return False
