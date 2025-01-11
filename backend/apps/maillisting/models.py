"""
Database Client related models
"""
import uuid

from django.db import models
from django.utils.translation import gettext as _


#  pylint: disable=duplicate-code
class Maillisting(models.Model):
    """
    Model representing the Maillisting entity.

    Attributes:
        id (UUIDField): The primary key for the model, automatically generated as a UUID.
        full_name (CharField): The full name field.
        email (EmailField): The email field.
        created_at (DateTimeField): The timestamp of when this instance was created.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=64, verbose_name=_('Full name'), null=True, blank=True)
    email = models.EmailField(max_length=128, verbose_name=_("Email"))
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name=_('Created at')
    )

    def __str__(self):
        return f"{self.email}"

    class Meta:
        """
        Metadata options for the Maillisting model.
        Attributes:
            verbose_name (str): A human-readable name for the model in singular form.
            verbose_name_plural (str): A human-readable name for the model in plural form.
        """
        verbose_name = _('Maillisting')
        verbose_name_plural = _('Maillistings')
