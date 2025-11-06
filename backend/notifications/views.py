from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    """
    ViewSet pentru notificări
    GET /api/notifications - listează toate notificările user-ului curent
    POST /api/notifications/{id}/mark_as_read - marchează ca citită
    POST /api/notifications/mark_all_as_read - marchează toate ca citite
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return only notifications for current user
        """
        return Notification.objects.filter(user=self.request.user.profile)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """
        Mark a single notification as read
        """
        notification = self.get_object()
        notification.mark_as_read()
        return Response({'status': 'notification marked as read'})

    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        """
        Mark all notifications as read for current user
        """
        notifications = self.get_queryset().filter(citit=False)
        count = notifications.count()

        from django.utils import timezone
        notifications.update(citit=True, data_citire=timezone.now())

        return Response({
            'status': 'all notifications marked as read',
            'count': count
        })

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """
        Get count of unread notifications
        """
        count = self.get_queryset().filter(citit=False).count()
        return Response({'unread_count': count})
