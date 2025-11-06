from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer pentru notificări
    """
    class Meta:
        model = Notification
        fields = ['id', 'user', 'tip', 'titlu', 'mesaj', 'link', 'citit', 'data_creare', 'data_citire']
        read_only_fields = ['id', 'user', 'data_creare', 'data_citire']
