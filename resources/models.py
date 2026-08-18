from django.db import models
from django.conf import settings
from planner.models import Subject


class Resource(models.Model):
    TYPE_CHOICES = [
        ('article', 'Article'),
        ('video', 'Video'),
        ('book', 'Book'),
        ('course', 'Course'),
        ('tool', 'Tool'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resources')
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name='resources')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    link = models.URLField()
    resource_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='article')
    thumbnail = models.ImageField(upload_to='resource_thumbs/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
