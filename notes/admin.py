from django.contrib import admin
from .models import Note, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name',)


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'subject', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_filter = ('categories', 'subject')
    filter_horizontal = ('categories',)
