from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from itertools import chain
from django.db.models import Count
import json

from planner.models import Task, Subject
from notes.models import Note, Category
from resources.models import Resource


@login_required
def home(request):
    user = request.user
    tasks = Task.objects.filter(user=user)
    notes = Note.objects.filter(user=user)
    resources = Resource.objects.filter(user=user)

    total_tasks = tasks.count()
    total_notes = notes.count()
    total_resources = resources.count()
    completed_tasks = tasks.filter(is_completed=True).count()
    pending_tasks = total_tasks - completed_tasks
    progress_percent = round((completed_tasks / total_tasks) * 100) if total_tasks else 0
    upcoming_tasks = tasks.filter(is_completed=False, due_date__gte=timezone.now().date()).order_by('due_date')[:5]

    # Recent activity: merge the 5 most recent of each model into one timeline
    recent_tasks = [{'type': 'Task', 'title': t.title, 'time': t.updated_at, 'url': None} for t in tasks.order_by('-updated_at')[:5]]
    recent_notes = [{'type': 'Note', 'title': n.title, 'time': n.updated_at, 'url': n.get_absolute_url()} for n in notes.order_by('-updated_at')[:5]]
    recent_resources = [{'type': 'Resource', 'title': r.title, 'time': r.created_at, 'url': None} for r in resources.order_by('-created_at')[:5]]
    recent_activity = sorted(
        chain(recent_tasks, recent_notes, recent_resources),
        key=lambda x: x['time'], reverse=True
    )[:8]

    # Chart data: tasks by priority (for Chart.js on the dashboard)
    priority_counts = {
        'low': tasks.filter(priority='low').count(),
        'medium': tasks.filter(priority='medium').count(),
        'high': tasks.filter(priority='high').count(),
    }

    # Chart data: notes grouped by category (for Chart.js on the dashboard)
    category_counts = (
        Category.objects.filter(user=user)
        .annotate(note_count=Count('notes'))
        .order_by('-note_count')
    )
    notes_by_category_labels = [c.name for c in category_counts]
    notes_by_category_data = [c.note_count for c in category_counts]
    uncategorized_count = notes.filter(categories__isnull=True).distinct().count()
    if uncategorized_count:
        notes_by_category_labels.append('Uncategorized')
        notes_by_category_data.append(uncategorized_count)

    context = {
        'total_tasks': total_tasks,
        'total_notes': total_notes,
        'total_resources': total_resources,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'progress_percent': progress_percent,
        'upcoming_tasks': upcoming_tasks,
        'recent_activity': recent_activity,
        'priority_counts': priority_counts,
        'notes_by_category_labels': json.dumps(notes_by_category_labels),
        'notes_by_category_data': json.dumps(notes_by_category_data),
        'subjects_count': Subject.objects.filter(user=user).count(),
    }
    return render(request, 'dashboard/home.html', context)
