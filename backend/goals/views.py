from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Goal, UserGoal
from .serializers import (
    GoalSerializer,
    UserGoalSerializer,
    UserGoalCreateSerializer,
    UserGoalProgressSerializer
)
from notifications.models import Notification


class GoalViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for goal templates
    GET /api/goals - List all active goal templates
    GET /api/goals/{id} - Get specific goal template
    """
    queryset = Goal.objects.filter(is_active=True)
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]


class UserGoalViewSet(viewsets.ModelViewSet):
    """
    ViewSet for user goals
    GET /api/user_goals - List user's goals
    POST /api/user_goals - Create new goal for user
    GET /api/user_goals/{id} - Get specific user goal
    """
    serializer_class = UserGoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter to show only current user's goals"""
        return UserGoal.objects.filter(user=self.request.user.profile)

    def get_serializer_class(self):
        """Use different serializer for creation"""
        if self.action == 'create':
            return UserGoalCreateSerializer
        return UserGoalSerializer

    def perform_create(self, serializer):
        """Create user goal and set the user"""
        goal_id = serializer.validated_data['goal_id']
        goal = Goal.objects.get(id=goal_id)

        # Check if user already has an active goal of this type
        existing_goal = UserGoal.objects.filter(
            user=self.request.user.profile,
            goal=goal,
            status='active'
        ).first()

        if existing_goal:
            raise serializers.ValidationError({
                'error': 'You already have an active goal of this type'
            })

        serializer.save(user=self.request.user.profile, goal=goal)

    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Get user's active goals
        GET /api/user_goals/active/
        """
        goals = self.get_queryset().filter(status='active')
        serializer = UserGoalProgressSerializer(goals, many=True)
        return Response({
            'count': goals.count(),
            'goals': serializer.data
        })

    @action(detail=False, methods=['get'])
    def completed(self, request):
        """
        Get user's completed goals
        GET /api/user_goals/completed/
        """
        goals = self.get_queryset().filter(status='completed')
        serializer = UserGoalProgressSerializer(goals, many=True)
        return Response({
            'count': goals.count(),
            'goals': serializer.data
        })

    @action(detail=True, methods=['post'])
    def increment(self, request, pk=None):
        """
        Increment goal progress
        POST /api/user_goals/{id}/increment/
        Body: { "amount": 1 }
        """
        user_goal = self.get_object()

        # Check ownership
        if user_goal.user != request.user.profile:
            return Response({
                'error': 'You can only update your own goals'
            }, status=status.HTTP_403_FORBIDDEN)

        # Check if goal is active
        if user_goal.status != 'active':
            return Response({
                'error': f'Goal is {user_goal.status}, cannot update progress'
            }, status=status.HTTP_400_BAD_REQUEST)

        amount = request.data.get('amount', 1)
        completed = user_goal.increment_progress(amount)

        if completed:
            # Create completion notification
            Notification.objects.create(
                user=request.user.profile,
                tip='goal_completed',
                titlu=f'Goal Completed! {user_goal.goal.icon}',
                mesaj=f'You completed: {user_goal.goal.name}',
                link='/goals'
            )

        return Response({
            'status': 'success',
            'completed': completed,
            'goal': UserGoalProgressSerializer(user_goal).data
        })

    @action(detail=True, methods=['post'])
    def update_streak(self, request, pk=None):
        """
        Update workout streak for streak-type goals
        POST /api/user_goals/{id}/update_streak/
        """
        user_goal = self.get_object()

        # Check ownership
        if user_goal.user != request.user.profile:
            return Response({
                'error': 'You can only update your own goals'
            }, status=status.HTTP_403_FORBIDDEN)

        # Check if it's a streak goal
        if user_goal.goal.goal_type != 'workout_streak':
            return Response({
                'error': 'This goal is not a streak-type goal'
            }, status=status.HTTP_400_BAD_REQUEST)

        completed = user_goal.update_streak()

        if completed:
            # Create completion notification
            Notification.objects.create(
                user=request.user.profile,
                tip='goal_completed',
                titlu=f'Goal Completed! {user_goal.goal.icon}',
                mesaj=f'You completed: {user_goal.goal.name}',
                link='/goals'
            )

        return Response({
            'status': 'success',
            'completed': completed,
            'current_streak': user_goal.current_streak,
            'goal': UserGoalProgressSerializer(user_goal).data
        })

    @action(detail=True, methods=['post'])
    def abandon(self, request, pk=None):
        """
        Abandon goal
        POST /api/user_goals/{id}/abandon/
        """
        user_goal = self.get_object()

        # Check ownership
        if user_goal.user != request.user.profile:
            return Response({
                'error': 'You can only abandon your own goals'
            }, status=status.HTTP_403_FORBIDDEN)

        user_goal.abandon()

        return Response({
            'status': 'success',
            'message': 'Goal abandoned',
            'goal': UserGoalProgressSerializer(user_goal).data
        })

    @action(detail=False, methods=['post'])
    def check_expired(self, request):
        """
        Check and mark expired goals as failed
        POST /api/user_goals/check_expired/
        """
        expired_goals = self.get_queryset().filter(
            status='active',
            deadline__lt=timezone.now()
        )

        failed_count = 0
        for goal in expired_goals:
            goal.fail()
            failed_count += 1

        return Response({
            'status': 'success',
            'failed_count': failed_count,
            'message': f'{failed_count} goal(s) marked as failed'
        })

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Get user's goal statistics
        GET /api/user_goals/stats/
        """
        user_goals = self.get_queryset()

        stats = {
            'total': user_goals.count(),
            'active': user_goals.filter(status='active').count(),
            'completed': user_goals.filter(status='completed').count(),
            'failed': user_goals.filter(status='failed').count(),
            'completion_rate': 0,
        }

        total_finished = stats['completed'] + stats['failed']
        if total_finished > 0:
            stats['completion_rate'] = int((stats['completed'] / total_finished) * 100)

        return Response(stats)
