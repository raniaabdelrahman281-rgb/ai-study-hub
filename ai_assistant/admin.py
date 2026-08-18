from django.contrib import admin
from .models import AIConversation


@admin.register(AIConversation)
class AIConversationAdmin(admin.ModelAdmin):
    list_display = ('user', 'feature', 'note', 'created_at')
    list_filter = ('feature',)
    search_fields = ('prompt', 'response', 'user__username')
