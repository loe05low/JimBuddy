from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Sesiune, Cerere, SessionParticipant
from .serializers import (
    SesiuneSerializer,
    SesiuneCreateSerializer,
    SessionParticipantSerializer,
    CerereSerializer,
    CerereUpdateSerializer
)


class SesiuneViewSet(viewsets.ModelViewSet):
    """
    ViewSet pentru sesiuni de antrenament
    GET /api/sesiuni?status=activ - listează sesiuni active
    POST /api/sesiuni - creează sesiune nouă
    GET /api/sesiuni/{id} - detalii sesiune
    """
    queryset = Sesiune.objects.all()
    serializer_class = SesiuneSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filtrează sesiuni după status, tip, oraș, și dată
        Exclude sesiuni anulate (doar pentru owner în my_sessions)
        Exclude sesiuni private dacă nu ești prieten
        """
        from users.models import BlockedUser
        from social.models import Follow

        queryset = Sesiune.objects.all()
        user_profile = self.request.user.profile if self.request.user.is_authenticated else None

        # Exclude sesiuni create de utilizatori blocați
        if user_profile:
            blocked_ids = BlockedUser.objects.filter(blocker=user_profile).values_list('blocked_id', flat=True)
            queryset = queryset.exclude(user_id__in=blocked_ids)

        # Exclude sesiuni anulate din listare publică
        queryset = queryset.exclude(status='anulat')

        # Filtre
        status_filter = self.request.query_params.get('status', None)
        tip_filter = self.request.query_params.get('tip', None)
        city_filter = self.request.query_params.get('city', None)
        date_filter = self.request.query_params.get('date', None)

        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if tip_filter:
            queryset = queryset.filter(tip_antrenament__icontains=tip_filter)
        if city_filter:
            queryset = queryset.filter(city__icontains=city_filter)
        if date_filter:
            queryset = queryset.filter(data_sesiune__date=date_filter)

        # Sortare după data sesiunii (closest first) dacă există
        sort = self.request.query_params.get('sort', 'created')
        if sort == 'closest' and queryset.filter(data_sesiune__isnull=False).exists():
            queryset = queryset.filter(data_sesiune__gte=timezone.now()).order_by('data_sesiune')
        else:
            queryset = queryset.order_by('-data_creare')

        return queryset

    def get_serializer_class(self):
        """
        Folosește serializer diferit pentru create
        """
        if self.action == 'create':
            return SesiuneCreateSerializer
        return SesiuneSerializer

    def perform_create(self, serializer):
        """
        Setează user-ul curent ca owner al sesiunii
        """
        serializer.save(user=self.request.user.profile)

    @action(detail=False, methods=['get'])
    def my_sessions(self, request):
        """
        Obține sesiunile create de user-ul curent
        GET /api/sesiuni/my_sessions
        """
        sesiuni = Sesiune.objects.filter(user=request.user.profile).order_by('-data_creare')
        serializer = self.get_serializer(sesiuni, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def complete_session(self, request, pk=None):
        """
        Marchează sesiunea ca fiind completată și actualizează automat:
        - Număr antrenamente
        - Streak
        - Goals progress
        - Achievements
        POST /api/sesiuni/{id}/complete_session/
        """
        sesiune = self.get_object()

        # Verifică că user-ul este owner-ul sesiunii
        if sesiune.user != request.user.profile:
            return Response({
                'error': 'Doar owner-ul sesiunii poate completa sesiunea',
                'code': 403
            }, status=status.HTTP_403_FORBIDDEN)

        try:
            from datetime import date, timedelta
            from achievements.utils import check_and_unlock_achievements
            from goals.models import UserGoal

            sesiune.complete()
            profile = request.user.profile

            # 1. Update workout count
            profile.nr_antrenamente += 1

            # 2. Update streak automatically
            today = date.today()
            if profile.last_workout_date:
                if profile.last_workout_date == today:
                    # Already worked out today, don't change streak
                    pass
                elif profile.last_workout_date == today - timedelta(days=1):
                    # Consecutive day
                    profile.current_streak += 1
                    profile.last_workout_date = today
                else:
                    # Streak broken
                    profile.current_streak = 1
                    profile.last_workout_date = today
            else:
                # First workout ever
                profile.current_streak = 1
                profile.last_workout_date = today

            profile.save(update_fields=['nr_antrenamente', 'current_streak', 'last_workout_date'])

            # 3. Create activity log
            from social.models import ActivityLog
            ActivityLog.objects.create(
                user=profile,
                activity_type='workout_completed',
                description=f'{profile.nume} completed a {sesiune.tip_antrenament} workout at {sesiune.sala.nume}'
            )

            # 4. Update goals progress automatically
            workout_goals = UserGoal.objects.filter(
                user=profile,
                status='active',
                goal__goal_type='workout'
            )
            for user_goal in workout_goals:
                user_goal.current_value += 1
                if user_goal.current_value >= user_goal.target_value:
                    user_goal.status = 'completed'
                user_goal.save()

            # Update streak goals
            streak_goals = UserGoal.objects.filter(
                user=profile,
                status='active',
                goal__goal_type='streak'
            )
            for user_goal in streak_goals:
                user_goal.current_value = profile.current_streak
                if user_goal.current_value >= user_goal.target_value:
                    user_goal.status = 'completed'
                user_goal.save()

            # 5. Check and unlock achievements automatically
            check_and_unlock_achievements(profile)

            return Response({
                'status': 'success',
                'message': 'Sesiune completată! 💪',
                'session': SesiuneSerializer(sesiune, context={'request': request}).data,
                'streak': profile.current_streak,
                'total_workouts': profile.nr_antrenamente
            })
        except ValueError as e:
            return Response({
                'error': str(e),
                'code': 400
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def cancel_session(self, request, pk=None):
        """
        Anulează sesiunea
        POST /api/sesiuni/{id}/cancel_session/
        """
        sesiune = self.get_object()

        # Verifică că user-ul este owner-ul sesiunii
        if sesiune.user != request.user.profile:
            return Response({
                'error': 'Doar owner-ul sesiunii poate anula sesiunea',
                'code': 403
            }, status=status.HTTP_403_FORBIDDEN)

        try:
            sesiune.cancel()
            return Response({
                'status': 'success',
                'message': 'Sesiune anulată',
                'session': SesiuneSerializer(sesiune, context={'request': request}).data
            })
        except ValueError as e:
            return Response({
                'error': str(e),
                'code': 400
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        """
        Alătură-te la sesiune
        POST /api/sesiuni/{id}/join/
        """
        sesiune = self.get_object()
        profile = request.user.profile

        # Verificări
        if sesiune.user == profile:
            return Response({'error': 'Ești owner-ul acestei sesiuni'}, status=400)

        if sesiune.status != 'activ':
            return Response({'error': 'Sesiunea nu este activă'}, status=400)

        # Verifică limita de participanți
        current_count = sesiune.participants.count()
        if current_count >= sesiune.max_participants:
            return Response({'error': 'Sesiunea este plină'}, status=400)

        # Adaugă participant
        participant, created = SessionParticipant.objects.get_or_create(
            sesiune=sesiune,
            user=profile
        )

        if created:
            # Creează notificare pentru owner
            from notifications.models import Notification
            Notification.objects.create(
                user=sesiune.user,
                notification_type='session_joined',
                title=f'{profile.nume} s-a alăturat sesiunii tale',
                message=f'{profile.nume} s-a alăturat la sesiunea ta de {sesiune.tip_antrenament}'
            )

            return Response({
                'message': 'Te-ai alăturat cu succes!',
                'session': SesiuneSerializer(sesiune, context={'request': request}).data
            }, status=201)
        else:
            return Response({'message': 'Ești deja participant'}, status=200)

    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        """
        Părăsește sesiunea
        POST /api/sesiuni/{id}/leave/
        """
        sesiune = self.get_object()
        profile = request.user.profile

        SessionParticipant.objects.filter(sesiune=sesiune, user=profile).delete()

        return Response({'message': 'Ai părăsit sesiunea'}, status=200)

    @action(detail=True, methods=['post'])
    def repeat(self, request, pk=None):
        """
        Repetă sesiunea (creează una nouă cu aceleași detalii)
        POST /api/sesiuni/{id}/repeat/
        Body: {data_sesiune, interval_orar}
        """
        old_session = self.get_object()

        # Verifică că user-ul este owner-ul sesiunii
        if old_session.user != request.user.profile:
            return Response({'error': 'Doar owner-ul poate repeta sesiunea'}, status=403)

        # Creează sesiune nouă
        new_session = Sesiune.objects.create(
            user=request.user.profile,
            sala=old_session.sala,
            tip_antrenament=old_session.tip_antrenament,
            interval_orar=request.data.get('interval_orar', old_session.interval_orar),
            data_sesiune=request.data.get('data_sesiune'),
            city=old_session.city,
            descriere=old_session.descriere,
            private=old_session.private,
            max_participants=old_session.max_participants,
            status='activ'
        )

        return Response({
            'message': 'Sesiune repetată cu succes',
            'session': SesiuneSerializer(new_session, context={'request': request}).data
        }, status=201)

    @action(detail=False, methods=['get'])
    def history(self, request):
        """
        Obține istoricul sesiunilor completate de user
        GET /api/sesiuni/history/
        """
        completed = Sesiune.objects.filter(
            user=request.user.profile,
            status='completat'
        ).order_by('-data_creare')

        serializer = SesiuneSerializer(completed, many=True, context={'request': request})
        return Response({'sessions': serializer.data})


class CerereViewSet(viewsets.ModelViewSet):
    """
    ViewSet pentru cereri de gym buddy
    GET /api/cereri - listează cereri (filtrare automată)
    POST /api/cereri - trimite cerere nouă
    PATCH /api/cereri/{id} - acceptă/refuză cerere
    """
    queryset = Cerere.objects.all()
    serializer_class = CerereSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filtrează cereri:
        - User vede cererile trimise de el
        - User vede cererile primite pentru sesiunile lui
        """
        user_profile = self.request.user.profile

        # Cereri trimise de user
        sent = Cerere.objects.filter(applicant=user_profile)

        # Cereri primite pentru sesiunile user-ului
        received = Cerere.objects.filter(sesiune__user=user_profile)

        return (sent | received).distinct().order_by('-data_creare')

    def get_serializer_class(self):
        """
        Folosește serializer diferit pentru update
        """
        if self.action in ['update', 'partial_update']:
            return CerereUpdateSerializer
        return CerereSerializer

    def perform_create(self, serializer):
        """
        Setează applicant-ul ca user-ul curent
        """
        serializer.save(applicant=self.request.user.profile)

    def update(self, request, *args, **kwargs):
        """
        Permite doar owner-ului sesiunii să accepte/refuze
        """
        cerere = self.get_object()

        # Verifică că user-ul este owner-ul sesiunii
        if cerere.sesiune.user != request.user.profile:
            return Response({
                'error': 'Doar owner-ul sesiunii poate accepta/refuza cereri',
                'code': 403
            }, status=status.HTTP_403_FORBIDDEN)

        # Actualizează status-ul
        serializer = self.get_serializer(cerere, data=request.data, partial=True)
        if serializer.is_valid():
            new_status = serializer.validated_data['status']
            if new_status == 'acceptat':
                cerere.accept()
            else:
                cerere.reject()

            return Response(CerereSerializer(cerere).data)

        return Response({
            'error': serializer.errors,
            'code': 400
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def my_sent_requests(self, request):
        """
        Obține cererile trimise de user-ul curent
        GET /api/cereri/my_sent_requests
        """
        cereri = Cerere.objects.filter(applicant=request.user.profile).order_by('-data_creare')
        serializer = self.get_serializer(cereri, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_received_requests(self, request):
        """
        Obține cererile primite pentru sesiunile user-ului curent
        GET /api/cereri/my_received_requests
        """
        cereri = Cerere.objects.filter(sesiune__user=request.user.profile).order_by('-data_creare')
        serializer = self.get_serializer(cereri, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def accept_request(self, request, pk=None):
        """
        Acceptă o cerere de gym buddy
        PATCH /api/cereri/{id}/accept_request
        """
        cerere = self.get_object()

        # Verifică că user-ul este owner-ul sesiunii
        if cerere.sesiune.user != request.user.profile:
            return Response({
                'error': 'Doar owner-ul sesiunii poate accepta cereri',
                'code': 403
            }, status=status.HTTP_403_FORBIDDEN)

        cerere.accept()
        return Response(CerereSerializer(cerere).data)

    @action(detail=True, methods=['patch'])
    def reject_request(self, request, pk=None):
        """
        Refuză o cerere de gym buddy
        PATCH /api/cereri/{id}/reject_request
        """
        cerere = self.get_object()

        # Verifică că user-ul este owner-ul sesiunii
        if cerere.sesiune.user != request.user.profile:
            return Response({
                'error': 'Doar owner-ul sesiunii poate refuza cereri',
                'code': 403
            }, status=status.HTTP_403_FORBIDDEN)

        cerere.reject()
        return Response(CerereSerializer(cerere).data)
