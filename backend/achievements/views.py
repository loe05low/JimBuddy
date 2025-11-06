from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, F
from .models import Achievement, UserAchievement
from .serializers import (
    AchievementSerializer,
    UserAchievementSerializer,
    UserAchievementProgressSerializer
)
from .utils import check_and_unlock_achievements


class AchievementViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for achievements
    GET /api/achievements - List all achievements
    GET /api/achievements/{id} - Get achievement details
    """
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def my_achievements(self, request):
        """
        Get current user's achievements with progress
        GET /api/achievements/my_achievements/
        """
        user_profile = request.user.profile

        # Get all user achievements (unlocked and in progress)
        user_achievements = UserAchievement.objects.filter(user=user_profile)
        serializer = UserAchievementProgressSerializer(user_achievements, many=True)

        # Calculate stats
        total_achievements = Achievement.objects.count()
        unlocked_count = user_achievements.filter(progress__gte=F('achievement__required_count')).count()
        total_xp = sum(
            ua.achievement.xp_reward
            for ua in user_achievements
            if ua.is_unlocked
        )

        return Response({
            'achievements': serializer.data,
            'stats': {
                'total': total_achievements,
                'unlocked': unlocked_count,
                'in_progress': user_achievements.count() - unlocked_count,
                'total_xp': total_xp,
            }
        })

    @action(detail=False, methods=['post'])
    def check_achievements(self, request):
        """
        Manually trigger achievement check for current user
        POST /api/achievements/check_achievements/
        """
        user_profile = request.user.profile
        newly_unlocked = check_and_unlock_achievements(user_profile)

        if newly_unlocked:
            return Response({
                'status': 'success',
                'message': f'Unlocked {len(newly_unlocked)} new achievement(s)! 🏆',
                'achievements': UserAchievementSerializer(newly_unlocked, many=True).data
            })
        else:
            return Response({
                'status': 'success',
                'message': 'No new achievements unlocked',
                'achievements': []
            })

    @action(detail=False, methods=['get'])
    def categories(self, request):
        """
        Get achievements grouped by category
        GET /api/achievements/categories/
        """
        categories = Achievement.CATEGORY_CHOICES
        user_profile = request.user.profile

        result = {}
        for category_key, category_name in categories:
            achievements = Achievement.objects.filter(category=category_key)

            # Get user's progress for these achievements
            user_achievements = UserAchievement.objects.filter(
                user=user_profile,
                achievement__category=category_key
            )

            result[category_key] = {
                'name': category_name,
                'total': achievements.count(),
                'unlocked': sum(1 for ua in user_achievements if ua.is_unlocked),
                'achievements': UserAchievementProgressSerializer(user_achievements, many=True).data
            }

        return Response(result)
