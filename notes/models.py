from django.db import models
from django.conf import settings
from django.urls import reverse
from planner.models import Subject


class Category(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=80)

    class Meta:
        ordering = ['name']
        unique_together = ('user', 'name')
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Note(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notes')
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name='notes')
    categories = models.ManyToManyField(Category, blank=True, related_name='notes')
    title = models.CharField(max_length=200)
    content = models.TextField()
    ai_summary = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('notes:note_detail', kwargs={'pk': self.pk})
