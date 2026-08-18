from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Q
from django.http import JsonResponse

from .models import Note, Category
from .forms import NoteForm, CategoryForm


@login_required
def note_list(request):
    notes = Note.objects.filter(user=request.user)

    category_id = request.GET.get('category')
    if category_id:
        notes = notes.filter(categories__id=category_id)

    query = request.GET.get('q')
    if query:
        notes = notes.filter(Q(title__icontains=query) | Q(content__icontains=query))

    notes = notes.distinct()
    paginator = Paginator(notes, settings.PAGINATE_BY)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'notes/note_list.html', {
        'page_obj': page_obj,
        'categories': Category.objects.filter(user=request.user),
        'query': query or '',
    })


@login_required
def note_search_api(request):
    """Lightweight JSON endpoint used by the live-search JS (no DRF)."""
    query = request.GET.get('q', '')
    notes = Note.objects.filter(user=request.user)
    if query:
        notes = notes.filter(Q(title__icontains=query) | Q(content__icontains=query))
    notes = notes[:10]
    data = [
        {
            'id': n.id,
            'title': n.title,
            'snippet': (n.content[:100] + '...') if len(n.content) > 100 else n.content,
            'url': n.get_absolute_url(),
        }
        for n in notes
    ]
    return JsonResponse({'results': data})


@login_required
def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    return render(request, 'notes/note_detail.html', {'note': note})


@login_required
def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST, user=request.user)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            form.save_m2m()
            messages.success(request, 'Note created.')
            return redirect('notes:note_detail', pk=note.pk)
    else:
        form = NoteForm(user=request.user)
    return render(request, 'notes/note_form.html', {'form': form, 'title': 'New Note'})


@login_required
def note_update(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Note updated.')
            return redirect('notes:note_detail', pk=note.pk)
    else:
        form = NoteForm(instance=note, user=request.user)
    return render(request, 'notes/note_form.html', {'form': form, 'title': 'Edit Note'})


@login_required
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Note deleted.')
        return redirect('notes:note_list')
    return render(request, 'notes/note_confirm_delete.html', {'note': note})


@login_required
def category_list(request):
    categories = Category.objects.filter(user=request.user)
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, 'Category added.')
            return redirect('notes:category_list')
    else:
        form = CategoryForm()
    return render(request, 'notes/category_list.html', {'categories': categories, 'form': form})


@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted.')
    return redirect('notes:category_list')
