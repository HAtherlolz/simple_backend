"""
The file contains the admin classes related with mailsender model for Django Admin Panel.
"""
from django.contrib import admin

from .models import MailSender


class MailSenderAdmin(admin.ModelAdmin):
    """
    Admin interface for the MailSender model.
    """
    list_display = ("subject", "created_at")  # Fields to display in the list view
    list_filter = ("created_at",)  # Filters in the admin sidebar
    search_fields = ("subject", "emails")  # Searchable fields
    readonly_fields = ("created_at",)  # Fields that are not editable
    # form = MailSenderForm
    fieldsets = (
        (None, {
            "fields": ("subject", "emails", "message")
        }),
        ("Timestamps", {
            "fields": ("created_at",),
        }),
    )


admin.site.register(MailSender, MailSenderAdmin)
