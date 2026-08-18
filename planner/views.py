from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.utils import timezone

from .models import Task, Subject
from .forms import TaskForm, SubjectForm


@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)

    status = request.GET.get('status')
    if status == 'completed':
        tasks = tasks.filter(is_completed=True)
    elif status == 'pending':
        tasks = tasks.filter(is_completed=False)

    priority = request.GET.get('priority')
    if priority in ('low', 'medium', 'high'):
        tasks = tasks.filter(priority=priority)

    query = request.GET.get('q')
    if query:
        tasks = tasks.filter(Q(title__icontains=query) | Q(description__icontains=query))

    paginator = Paginator(tasks, settings.PAGINATE_BY)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'planner/task_list.html', {
        'page_obj': page_obj,
        'subjects': Subject.objects.filter(user=request.user),
    })


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Task created.')
            return redirect('planner:task_list')
    else:
        form = TaskForm(user=request.user)
    return render(request, 'planner/task_form.html', {'form': form, 'title': 'Add Task'})


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated.')
            return redirect('planner:task_list')
    else:
        form = TaskForm(instance=task, user=request.user)
    return render(request, 'planner/task_form.html', {'form': form, 'title': 'Edit Task'})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted.')
        return redirect('planner:task_list')
    return render(request, 'planner/task_confirm_delete.html', {'task': task})


@login_required
def task_toggle_complete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.is_completed = not task.is_completed
    task.save()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'is_completed': task.is_completed})
    return redirect('planner:task_list')


@login_required
def task_export_pdf(request):
    """Export the current user's tasks (respecting the same filters as the
    list page) as a nicely formatted PDF."""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

    tasks = Task.objects.filter(user=request.user)

    status = request.GET.get('status')
    if status == 'completed':
        tasks = tasks.filter(is_completed=True)
    elif status == 'pending':
        tasks = tasks.filter(is_completed=False)

    priority = request.GET.get('priority')
    if priority in ('low', 'medium', 'high'):
        tasks = tasks.filter(priority=priority)

    query = request.GET.get('q')
    if query:
        tasks = tasks.filter(Q(title__icontains=query) | Q(description__icontains=query))

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="my_tasks.pdf"'

    doc = SimpleDocTemplate(
        response, pagesize=A4,
        topMargin=1.8 * cm, bottomMargin=1.8 * cm, leftMargin=2 * cm, rightMargin=2 * cm,
        title="My Tasks - AI Study Hub"
    )
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('TitleCustom', parent=styles['Title'], fontSize=20,
                                  textColor=colors.HexColor('#1F2937'))
    meta_style = ParagraphStyle('Meta', parent=styles['Normal'], fontSize=9,
                                 textColor=colors.HexColor('#6B7280'), spaceAfter=16)
    cell_style = ParagraphStyle('Cell', parent=styles['Normal'], fontSize=9, leading=12)
    header_style = ParagraphStyle('Header', parent=styles['Normal'], fontSize=9.5,
                                   textColor=colors.white, fontName='Helvetica-Bold')

    story = [
        Paragraph("AI Study Hub — My Tasks", title_style),
        Paragraph(
            f"Exported for {request.user.username} on {timezone.now():%B %d, %Y %H:%M} "
            f"&middot; {tasks.count()} task(s)",
            meta_style
        ),
    ]

    data = [[
        Paragraph("Title", header_style), Paragraph("Subject", header_style),
        Paragraph("Priority", header_style), Paragraph("Due Date", header_style),
        Paragraph("Status", header_style),
    ]]
    for task in tasks:
        data.append([
            Paragraph(task.title, cell_style),
            Paragraph(task.subject.name if task.subject else '—', cell_style),
            Paragraph(task.get_priority_display(), cell_style),
            Paragraph(str(task.due_date) if task.due_date else '—', cell_style),
            Paragraph('Completed' if task.is_completed else 'Pending', cell_style),
        ])

    if len(data) == 1:
        story.append(Paragraph("No tasks match the current filters.", styles['Normal']))
    else:
        table = Table(data, colWidths=[5.5 * cm, 3 * cm, 2.5 * cm, 2.5 * cm, 2.5 * cm], repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4F46E5')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D1D5DB')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9FAFB')]),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(table)

    doc.build(story)
    return response


@login_required
def subject_list(request):
    subjects = Subject.objects.filter(user=request.user)
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.user = request.user
            subject.save()
            messages.success(request, 'Subject added.')
            return redirect('planner:subject_list')
    else:
        form = SubjectForm()
    return render(request, 'planner/subject_list.html', {'subjects': subjects, 'form': form})


@login_required
def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk, user=request.user)
    if request.method == 'POST':
        subject.delete()
        messages.success(request, 'Subject deleted.')
    return redirect('planner:subject_list')
