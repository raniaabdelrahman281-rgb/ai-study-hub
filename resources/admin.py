from django.contrib import admin
from .models import Resource


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'resource_type', 'subject', 'created_at')
    list_filter = ('resource_type',)
    search_fields = ('title', 'description', 'link')
