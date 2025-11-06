from rest_framework import serializers
from .models import Achievement, UserAchievement


class AchievementSerializer(serializers.ModelSerializer):
    """
    Serializer for Achievement model
    """
    class Meta:
        model = Achievement
        fields = [
            'id',
            'name',
            'description',
            'icon',
            'category',
            'key',
            'required_count',
            'xp_reward',
            'rarity',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class UserAchievementSerializer(serializers.ModelSerializer):
    """
    Serializer for UserAchievement with achievement details
    """
    achievement = AchievementSerializer(read_only=True)
    is_unlocked = serializers.BooleanField(read_only=True)

    class Meta:
        model = UserAchievement
        fields = [
            'id',
            'user',
            'achievement',
            'progress',
            'is_unlocked',
            'unlocked_at',
        ]
        read_only_fields = ['id', 'user', 'unlocked_at']


class UserAchievementProgressSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for achievement progress display
    Shows achievement with user's progress
    """
    achievement_name = serializers.CharField(source='achievement.name', read_only=True)
    achievement_icon = serializers.CharField(source='achievement.icon', read_only=True)
    achievement_description = serializers.CharField(source='achievement.description', read_only=True)
    required_count = serializers.IntegerField(source='achievement.required_count', read_only=True)
    xp_reward = serializers.IntegerField(source='achievement.xp_reward', read_only=True)
    is_unlocked = serializers.BooleanField(read_only=True)

    class Meta:
        model = UserAchievement
        fields = [
            'id',
            'achievement_name',
            'achievement_icon',
            'achievement_description',
            'required_count',
            'progress',
            'is_unlocked',
            'xp_reward',
            'unlocked_at',
        ]
