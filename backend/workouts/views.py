from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Sesiune, Cerere
from .serializers import (
    SesiuneSerializer,
    SesiuneCreateSerializer,
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
        Filtrează sesiuni după status
        """
        queryset = Sesiune.objects.all()
        status_filter = self.request.query_params.get('status', None)

        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset.order_by('-data_creare')

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
