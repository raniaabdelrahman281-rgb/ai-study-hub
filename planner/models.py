from django.db import models
from django.conf import settings
from django.urls import reverse


class Subject(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=120)
    color = models.CharField(max_length=7, default='#4F46E5', help_text='Hex color for UI badges')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        unique_together = ('user', 'name')

    def __str__(self):
        return self.name


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['is_completed', 'due_date', '-priority']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('planner:task_detail', kwargs={'pk': self.pk})

    @property
    def is_overdue(self):
        from django.utils import timezone
        return bool(self.due_date and not self.is_completed and self.due_date < timezone.now().date())


class StudySession(models.Model):
    """A logged block of study time, optionally tied to a subject or task."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='study_sessions')
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name='study_sessions')
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True, related_name='study_sessions')
    started_at = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=25)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.user.username} - {self.duration_minutes}min ({self.started_at:%Y-%m-%d})"
