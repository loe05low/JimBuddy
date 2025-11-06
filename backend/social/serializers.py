from rest_framework import serializers
from .models import Follow, ActivityLog
from users.serializers import UserProfileSerializer


class FollowSerializer(serializers.ModelSerializer):
    """
    Serializer for Follow relationships
    """
    follower_details = UserProfileSerializer(source='follower', read_only=True)
    following_details = UserProfileSerializer(source='following', read_only=True)

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'follower_details', 'following', 'following_details', 'created_at']
        read_only_fields = ['id', 'follower', 'created_at']


class ActivityLogSerializer(serializers.ModelSerializer):
    """
    Serializer for activity feed
    """
    user_details = UserProfileSerializer(source='user', read_only=True)
    related_user_details = UserProfileSerializer(source='related_user', read_only=True)

    class Meta:
        model = ActivityLog
        fields = ['id', 'user', 'user_details', 'activity_type', 'description',
                  'related_user', 'related_user_details', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
