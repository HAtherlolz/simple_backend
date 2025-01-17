"""
Database Client related models
"""
import uuid

from django.db import models
from django.utils.translation import gettext as _


class Client(models.Model):
    """
    Model representing the Client entity.

    Attributes:
        id (UUIDField): The primary key for the model, automatically generated as a UUID.
        full_name (CharField): The clients full name.
        email (EmailField): The clients email address.
        message (TextField): The message from the client.
        updated_at (DateTimeField): The timestamp of the last update to this instance.
        created_at (DateTimeField): The timestamp of when this instance was created.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=64, verbose_name=_('Full name'))
    email = models.EmailField(
        max_length=128,
        verbose_name=_("Email")
    )
    phone_number = models.CharField(
        null=True,
        blank=True,
        max_length=15,
        verbose_name=_("Phone number")
    )
    message = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Message")
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name=_('Created at')
    )

    def __str__(self):
        return f"{self.email}"

    class Meta:
        """
        Metadata options for the Client model.

        Attributes:
            verbose_name (str): A human-readable name for the model in singular form.
            verbose_name_plural (str): A human-readable name for the model in plural form.
        """
        verbose_name = _('Connect with us Form')
        verbose_name_plural = _('Connect with us Forms')
