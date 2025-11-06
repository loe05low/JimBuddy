from rest_framework import serializers
from .models import Goal, UserGoal


class GoalSerializer(serializers.ModelSerializer):
    """
    Serializer for Goal template model
    """
    class Meta:
        model = Goal
        fields = [
            'id',
            'name',
            'description',
            'goal_type',
            'period',
            'target_value',
            'icon',
            'xp_reward',
            'duration_days',
            'is_active',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class UserGoalSerializer(serializers.ModelSerializer):
    """
    Serializer for UserGoal with goal details
    """
    goal = GoalSerializer(read_only=True)
    goal_id = serializers.UUIDField(write_only=True, required=True)
    progress_percentage = serializers.IntegerField(read_only=True)
    is_completed = serializers.BooleanField(read_only=True)
    is_expired = serializers.BooleanField(read_only=True)

    class Meta:
        model = UserGoal
        fields = [
            'id',
            'user',
            'goal',
            'goal_id',
            'current_value',
            'status',
            'progress_percentage',
            'is_completed',
            'is_expired',
            'start_date',
            'deadline',
            'completed_at',
            'current_streak',
            'last_streak_date',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'user', 'start_date', 'completed_at', 'created_at', 'updated_at']


class UserGoalCreateSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for creating user goals
    """
    goal_id = serializers.UUIDField(required=True)

    class Meta:
        model = UserGoal
        fields = ['goal_id', 'deadline']

    def validate_goal_id(self, value):
        """Validate that the goal exists"""
        try:
            Goal.objects.get(id=value, is_active=True)
        except Goal.DoesNotExist:
            raise serializers.ValidationError("Goal not found or is inactive")
        return value


class UserGoalProgressSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for displaying goal progress
    """
    goal_name = serializers.CharField(source='goal.name', read_only=True)
    goal_icon = serializers.CharField(source='goal.icon', read_only=True)
    goal_description = serializers.CharField(source='goal.description', read_only=True)
    target_value = serializers.IntegerField(source='goal.target_value', read_only=True)
    progress_percentage = serializers.IntegerField(read_only=True)

    class Meta:
        model = UserGoal
        fields = [
            'id',
            'goal_name',
            'goal_icon',
            'goal_description',
            'target_value',
            'current_value',
            'progress_percentage',
            'status',
            'deadline',
            'completed_at',
        ]
