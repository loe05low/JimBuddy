from rest_framework import serializers
from .models import Conversation, Message
from users.serializers import UserProfileSerializer
from workouts.serializers import SesiuneSerializer


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer pentru mesaje
    """
    sender_details = UserProfileSerializer(source='sender', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'sender_details', 'content', 'is_read', 'created_at']
        read_only_fields = ['id', 'sender', 'created_at']


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer pentru conversaii
    """
    user1_details = UserProfileSerializer(source='user1', read_only=True)
    user2_details = UserProfileSerializer(source='user2', read_only=True)
    sesiune_details = SesiuneSerializer(source='sesiune', read_only=True)
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'type', 'user1', 'user1_details', 'user2', 'user2_details',
                  'sesiune', 'sesiune_details', 'last_message', 'unread_count',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_last_message(self, obj):
        """
        Returneaz ultimul mesaj din conversaie
        """
        last_msg = obj.messages.last()
        if last_msg:
            return MessageSerializer(last_msg).data
        return None

    def get_unread_count(self, obj):
        """
        Returneaz numrul de mesaje necitite pentru user-ul curent
        """
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            return obj.messages.filter(is_read=False).exclude(sender=request.user.profile).count()
        return 0
