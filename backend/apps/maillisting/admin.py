"""
The file contains the admin classes related with maillisting model for Django Admin Panel.
"""
from django.contrib import admin

from .models import Maillisting


class MaillistingAdmin(admin.ModelAdmin):
    """
    Admin interface for the Maillisting model.

    Provides functionality to manage Client instances in the Django admin site.
    """
    list_display = ('full_name', 'email', 'created_at',)
    search_fields = ('full_name', 'email')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)


admin.site.register(Maillisting, MaillistingAdmin)
