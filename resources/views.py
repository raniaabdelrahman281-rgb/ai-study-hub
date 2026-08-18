from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Q

from .models import Resource
from .forms import ResourceForm


@login_required
def resource_list(request):
    resources = Resource.objects.filter(user=request.user)

    rtype = request.GET.get('type')
    if rtype:
        resources = resources.filter(resource_type=rtype)

    query = request.GET.get('q')
    if query:
        resources = resources.filter(Q(title__icontains=query) | Q(description__icontains=query))

    paginator = Paginator(resources, settings.PAGINATE_BY)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'resources/resource_list.html', {
        'page_obj': page_obj,
        'types': Resource.TYPE_CHOICES,
    })


@login_required
def resource_create(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.user = request.user
            resource.save()
            messages.success(request, 'Resource added.')
            return redirect('resources:resource_list')
    else:
        form = ResourceForm(user=request.user)
    return render(request, 'resources/resource_form.html', {'form': form, 'title': 'Add Resource'})


@login_required
def resource_update(request, pk):
    resource = get_object_or_404(Resource, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES, instance=resource, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Resource updated.')
            return redirect('resources:resource_list')
    else:
        form = ResourceForm(instance=resource, user=request.user)
    return render(request, 'resources/resource_form.html', {'form': form, 'title': 'Edit Resource'})


@login_required
def resource_delete(request, pk):
    resource = get_object_or_404(Resource, pk=pk, user=request.user)
    if request.method == 'POST':
        resource.delete()
        messages.success(request, 'Resource deleted.')
        return redirect('resources:resource_list')
    return render(request, 'resources/resource_confirm_delete.html', {'resource': resource})
