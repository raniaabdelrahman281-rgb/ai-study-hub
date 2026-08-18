from django.db import models
from django.conf import settings
from notes.models import Note


class AIConversation(models.Model):
    FEATURE_CHOICES = [
        ('chat', 'Chat Assistant'),
        ('summarize', 'Summarize Note'),
        ('quiz', 'Generate Quiz'),
        ('flashcards', 'Generate Flashcards'),
        ('explain_error', 'Explain Programming Error'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ai_conversations')
    note = models.ForeignKey(Note, on_delete=models.SET_NULL, null=True, blank=True, related_name='ai_conversations')
    feature = models.CharField(max_length=20, choices=FEATURE_CHOICES, default='chat')
    prompt = models.TextField()
    response = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_feature_display()} - {self.user.username} ({self.created_at:%Y-%m-%d %H:%M})"
