from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet pentru conversații de chat
    """
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Returnează conversațiile user-ului curent
        """
        user_profile = self.request.user.profile
        return Conversation.objects.filter(
            user1=user_profile
        ) | Conversation.objects.filter(
            user2=user_profile
        ) | Conversation.objects.filter(
            sesiune__participants__user=user_profile
        ).distinct()

    @action(detail=False, methods=['post'])
    def create_private(self, request):
        """
        Creează conversație privată cu alt user
        POST /api/conversations/create_private/
        Body: {other_user_id}
        """
        other_user_id = request.data.get('other_user_id')
        from users.models import UserProfile

        try:
            other_user = UserProfile.objects.get(id=other_user_id)
        except UserProfile.DoesNotExist:
            return Response({'error': 'Utilizator negăsit'}, status=404)

        # Verifică dacă există deja conversație
        conversation = Conversation.objects.filter(
            type='private',
            user1__in=[request.user.profile, other_user],
            user2__in=[request.user.profile, other_user]
        ).first()

        if conversation:
            return Response(ConversationSerializer(conversation, context={'request': request}).data)

        # Creează conversație nouă
        conversation = Conversation.objects.create(
            type='private',
            user1=request.user.profile,
            user2=other_user
        )

        return Response(ConversationSerializer(conversation, context={'request': request}).data, status=201)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet pentru mesaje
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Returnează mesajele conversației specificate
        """
        conversation_id = self.request.query_params.get('conversation')
        if conversation_id:
            return Message.objects.filter(conversation_id=conversation_id).order_by('created_at')
        return Message.objects.none()

    def perform_create(self, serializer):
        """
        Setează sender-ul ca user-ul curent
        """
        serializer.save(sender=self.request.user.profile)
