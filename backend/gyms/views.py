from rest_framework import viewsets, permissions
from .models import Sala
from .serializers import SalaSerializer


class SalaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pentru săli (read-only pentru utilizatori, admin poate edita)
    GET /api/sali - listează toate sălile pentru hartă
    GET /api/sali/{id} - detalii sală
    """
    queryset = Sala.objects.all()
    serializer_class = SalaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
