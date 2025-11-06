from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from .models import Follow, ActivityLog
from .serializers import FollowSerializer, ActivityLogSerializer
from users.models import UserProfile
from users.serializers import UserProfileSerializer


class SocialViewSet(viewsets.ViewSet):
    """
    ViewSet for social features: follow, unfollow, followers, following, activity feed
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def follow(self, request):
        """
        Follow a user
        POST /api/social/follow/
        Body: { "user_id": "uuid" }
        """
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required'}, status=400)

        try:
            user_to_follow = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

        # Check if already following
        if Follow.objects.filter(follower=request.user.profile, following=user_to_follow).exists():
            return Response({'error': 'Already following this user'}, status=400)

        # Prevent self-follow
        if request.user.profile == user_to_follow:
            return Response({'error': 'Cannot follow yourself'}, status=400)

        # Create follow relationship
        follow = Follow.objects.create(
            follower=request.user.profile,
            following=user_to_follow
        )

        return Response({
            'status': 'success',
            'message': f'You are now following {user_to_follow.nume}',
            'follow': FollowSerializer(follow).data
        })

    @action(detail=False, methods=['post'])
    def unfollow(self, request):
        """
        Unfollow a user
        POST /api/social/unfollow/
        Body: { "user_id": "uuid" }
        """
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required'}, status=400)

        try:
            user_to_unfollow = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

        # Find and delete follow relationship
        try:
            follow = Follow.objects.get(
                follower=request.user.profile,
                following=user_to_unfollow
            )
            follow.delete()
            return Response({
                'status': 'success',
                'message': f'Unfollowed {user_to_unfollow.nume}'
            })
        except Follow.DoesNotExist:
            return Response({'error': 'Not following this user'}, status=400)

    @action(detail=False, methods=['get'])
    def followers(self, request):
        """
        Get list of followers for current user
        GET /api/social/followers/
        """
        followers = Follow.objects.filter(following=request.user.profile)
        serializer = FollowSerializer(followers, many=True)
        return Response({
            'count': followers.count(),
            'followers': serializer.data
        })

    @action(detail=False, methods=['get'])
    def following(self, request):
        """
        Get list of users current user is following
        GET /api/social/following/
        """
        following = Follow.objects.filter(follower=request.user.profile)
        serializer = FollowSerializer(following, many=True)
        return Response({
            'count': following.count(),
            'following': serializer.data
        })

    @action(detail=True, methods=['get'])
    def user_followers(self, request, pk=None):
        """
        Get followers for a specific user
        GET /api/social/{user_id}/user_followers/
        """
        try:
            user = UserProfile.objects.get(id=pk)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

        followers = Follow.objects.filter(following=user)
        serializer = FollowSerializer(followers, many=True)
        return Response({
            'count': followers.count(),
            'followers': serializer.data
        })

    @action(detail=True, methods=['get'])
    def user_following(self, request, pk=None):
        """
        Get following list for a specific user
        GET /api/social/{user_id}/user_following/
        """
        try:
            user = UserProfile.objects.get(id=pk)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

        following = Follow.objects.filter(follower=user)
        serializer = FollowSerializer(following, many=True)
        return Response({
            'count': following.count(),
            'following': serializer.data
        })

    @action(detail=False, methods=['get'])
    def activity_feed(self, request):
        """
        Get activity feed from users you follow
        GET /api/social/activity_feed/
        """
        # Get users current user is following
        following_users = Follow.objects.filter(
            follower=request.user.profile
        ).values_list('following', flat=True)

        # Get activities from those users (and own activities)
        activities = ActivityLog.objects.filter(
            Q(user__in=following_users) | Q(user=request.user.profile)
        )[:50]  # Limit to 50 most recent

        serializer = ActivityLogSerializer(activities, many=True)
        return Response({
            'count': activities.count(),
            'activities': serializer.data
        })

    @action(detail=False, methods=['get'])
    def suggestions(self, request):
        """
        Get friend suggestions based on:
        - Same fitness level
        - Similar rating
        - Not already following
        GET /api/social/suggestions/
        """
        current_user = request.user.profile

        # Get users already following
        already_following = Follow.objects.filter(
            follower=current_user
        ).values_list('following', flat=True)

        # Find similar users
        suggestions = UserProfile.objects.filter(
            grad=current_user.grad  # Same fitness level
        ).exclude(
            id=current_user.id  # Exclude self
        ).exclude(
            id__in=already_following  # Exclude already following
        ).order_by('-rating', '-nr_antrenamente')[:10]  # Top 10 by rating and workouts

        serializer = UserProfileSerializer(suggestions, many=True)
        return Response({
            'count': suggestions.count(),
            'suggestions': serializer.data
        })

    @action(detail=True, methods=['get'])
    def is_following(self, request, pk=None):
        """
        Check if current user is following a specific user
        GET /api/social/{user_id}/is_following/
        """
        try:
            user = UserProfile.objects.get(id=pk)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

        is_following = Follow.objects.filter(
            follower=request.user.profile,
            following=user
        ).exists()

        return Response({
            'is_following': is_following
        })
