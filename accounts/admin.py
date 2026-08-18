from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'university', 'major', 'is_email_verified', 'dark_mode')
    search_fields = ('user__username', 'user__email', 'university', 'major')
    list_filter = ('is_email_verified', 'dark_mode')
