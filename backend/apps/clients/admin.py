"""
The file contains the admin classes related with client model for Django Admin Panel.
"""
from django.contrib import admin

from .models import Client


class ClientAdmin(admin.ModelAdmin):
    """
    Admin interface for the Client model.

    Provides functionality to manage Client instances in the Django admin site.
    """
    list_display = ('full_name', 'email', 'phone_number', 'created_at')
    search_fields = ('full_name', 'email', 'phone_number')
    list_filter = ('created_at',)
    readonly_fields = ('id', 'created_at')
    ordering = ('-created_at',)


admin.site.register(Client, ClientAdmin)
