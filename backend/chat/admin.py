from django.contrib import admin
from .models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'get_participants', 'created_at']
    list_filter = ['type', 'created_at']
    search_fields = ['user1__nume', 'user2__nume', 'sesiune__tip_antrenament']

    def get_participants(self, obj):
        if obj.type == 'private':
            return f"{obj.user1.nume} & {obj.user2.nume}"
        return f"Group: {obj.sesiune.tip_antrenament}"
    get_participants.short_description = 'Participants'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'conversation', 'sender', 'content_preview', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['sender__nume', 'content']

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'
