from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Rating
from .serializers import RatingSerializer, RatingCreateSerializer


class RatingViewSet(viewsets.ModelViewSet):
    """
    ViewSet pentru rating-uri și comentarii
    GET /api/rating - listează toate rating-urile
    POST /api/rating - adaugă rating nou
    """
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """
        Folosește serializer diferit pentru create
        """
        if self.action == 'create':
            return RatingCreateSerializer
        return RatingSerializer

    def perform_create(self, serializer):
        """
        Setează from_user ca user-ul curent
        """
        serializer.save(from_user=self.request.user.profile)
