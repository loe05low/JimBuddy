from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import UserProfile
from .serializers import (
    UserProfileSerializer,
    UserProfileUpdateSerializer,
    UserRegistrationSerializer,
    UserSerializer,
    BlockedUserSerializer
)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Endpoint pentru înregistrare utilizator nou
    POST /api/auth/register
    Body: {username, email, password, password_confirm, nume, grad}
    """
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        # Generează JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'message': 'Utilizator înregistrat cu succes'
        }, status=status.HTTP_201_CREATED)

    return Response({
        'error': serializer.errors,
        'code': 400
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """
    Returnează informații despre user-ul autentificat
    GET /api/auth/me
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pentru profiluri utilizatori (read-only pentru alții)
    GET /api/profiles - listează toate profilurile
    GET /api/profiles/{id} - detalii profil + rating + comentarii
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['get'])
    def ratings(self, request, pk=None):
        """
        Obține toate rating-urile primite de un utilizator
        GET /api/profiles/{id}/ratings
        Ordonate descrescător după dată
        """
        profile = self.get_object()
        from ratings.models import Rating
        from ratings.serializers import RatingSerializer

        ratings = Rating.objects.filter(to_user=profile).order_by('-data')
        serializer = RatingSerializer(ratings, many=True)

        return Response({
            'user': UserProfileSerializer(profile).data,
            'ratings': serializer.data,
            'total_ratings': ratings.count()
        })

    @action(detail=True, methods=['get'])
    def sesiuni(self, request, pk=None):
        """
        Obține istoricul sesiunilor unui utilizator
        GET /api/profiles/{id}/sesiuni
        """
        profile = self.get_object()
        from workouts.models import Sesiune
        from workouts.serializers import SesiuneSerializer

        sesiuni = Sesiune.objects.filter(user=profile).order_by('-data_creare')
        serializer = SesiuneSerializer(sesiuni, many=True)

        return Response({
            'user': UserProfileSerializer(profile).data,
            'sesiuni': serializer.data,
            'total_sesiuni': sesiuni.count()
        })

    @action(detail=False, methods=['get', 'patch'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """
        Obține sau actualizează profilul utilizatorului curent
        GET /api/profiles/me - obține profil
        PATCH /api/profiles/me - actualizează profil (nume, bio, city, phone, grad, avatar)
        """
        profile = request.user.profile

        if request.method == 'GET':
            serializer = UserProfileSerializer(profile, context={'request': request})
            return Response(serializer.data)

        elif request.method == 'PATCH':
            serializer = UserProfileUpdateSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(UserProfileSerializer(profile, context={'request': request}).data)
            return Response({
                'error': serializer.errors,
                'code': 400
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def search(self, request):
        """
        Caută utilizatori după nume
        GET /api/profiles/search?q=nume
        """
        query = request.query_params.get('q', '')
        if len(query) < 2:
            return Response({'results': []})

        from .models import BlockedUser
        blocked_ids = BlockedUser.objects.filter(blocker=request.user.profile).values_list('blocked_id', flat=True)

        profiles = UserProfile.objects.filter(nume__icontains=query).exclude(
            id__in=blocked_ids
        ).exclude(id=request.user.profile.id)[:20]

        serializer = UserProfileSerializer(profiles, many=True, context={'request': request})
        return Response({'results': serializer.data})

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def block(self, request, pk=None):
        """
        Blochează un utilizator
        POST /api/profiles/{id}/block
        """
        from .models import BlockedUser

        profile_to_block = self.get_object()
        if profile_to_block == request.user.profile:
            return Response({'error': 'Nu te poți bloca pe tine însuți'}, status=400)

        blocked, created = BlockedUser.objects.get_or_create(
            blocker=request.user.profile,
            blocked=profile_to_block,
            defaults={'reason': request.data.get('reason', '')}
        )

        if created:
            return Response({'message': 'Utilizator blocat'}, status=201)
        return Response({'message': 'Utilizator deja blocat'}, status=200)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unblock(self, request, pk=None):
        """
        Deblochează un utilizator
        POST /api/profiles/{id}/unblock
        """
        from .models import BlockedUser

        profile_to_unblock = self.get_object()
        BlockedUser.objects.filter(
            blocker=request.user.profile,
            blocked=profile_to_unblock
        ).delete()

        return Response({'message': 'Utilizator deblocat'}, status=200)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def achievements(self, request, pk=None):
        """
        Obține achievement-urile unui utilizator
        GET /api/profiles/{id}/achievements
        """
        profile = self.get_object()
        from achievements.models import UserAchievement
        from achievements.serializers import UserAchievementSerializer

        user_achievements = UserAchievement.objects.filter(user=profile, unlocked=True).select_related('achievement')
        serializer = UserAchievementSerializer(user_achievements, many=True)

        return Response({'achievements': serializer.data})
