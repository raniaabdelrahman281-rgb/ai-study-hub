from django.contrib import admin
from .models import Subject, Task, StudySession


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'color', 'created_at')
    search_fields = ('name', 'user__username')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'subject', 'priority', 'due_date', 'is_completed')
    list_filter = ('priority', 'is_completed', 'subject')
    search_fields = ('title', 'description', 'user__username')


@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'task', 'started_at', 'duration_minutes')
    list_filter = ('subject',)
