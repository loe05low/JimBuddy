from rest_framework import serializers
from .models import Sala


class SalaSerializer(serializers.ModelSerializer):
    """
    Serializer pentru săli de fitness
    Include toate câmpurile necesare pentru afișare pe hartă
    """
    class Meta:
        model = Sala
        fields = ['id', 'nume', 'adresa', 'latitudine', 'longitudine', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
