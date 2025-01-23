"""
Database MailSender related models
"""
import uuid

from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _


from apps.core.utils import send_email


#  pylint: disable=duplicate-code
class MailSender(models.Model):
    """
    Model representing the MailSender entity.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject = models.CharField(
        max_length=128,
        verbose_name=_("Subject"),
        help_text=_("The subject of the email.")
    )
    emails = models.TextField(
        verbose_name=_("Emails"),
        help_text=_("Emails should be separated by comma. Example: 123@mail.com,1234@gmail.com")
    )
    message = models.TextField(
        verbose_name=_("Emails"),
        help_text=_("Emails should be separated by comma. Example: 123@mail.com,1234@gmail.com")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name=_('Created at')
    )

    def __str__(self):
        return f"{self.subject}, {str(self.created_at)}"

    class Meta:
        """
        Metadata options for the MailSender model.
        Attributes:
            verbose_name (str): A human-readable name for the model in singular form.
            verbose_name_plural (str): A human-readable name for the model in plural form.
        """
        verbose_name = _('MailSender')
        verbose_name_plural = _('MailSenders')

    def save(self, *args, **kwargs):
        """
        Override the default save method
        """
        emails = str(self.emails)
        recipient_list = emails.split(",")
        for recipient in recipient_list:
            send_email(
                subject=self.subject,
                message=self.message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[recipient]
            )
        super().save(*args, **kwargs)
