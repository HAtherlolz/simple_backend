"""
The file contains the encapsulated business logic for maillisting application.
"""
from django.conf import settings
from django.utils import timezone
from django.template.loader import render_to_string

from apps.clients.models import Client
from apps.core.utils import send_email_from_html

from .models import Maillisting
from .repository import MaillistingRepository


class MailListingService:
    """
    The service class for managing maillisting process.
    """
    _repo = MaillistingRepository

    @classmethod
    def maillisting(cls, client: Client) -> None:
        """
        Sends the emails for each in mail list.
        """
        emails_list = cls._repo.get_all()

        for maillisting in emails_list:
            SendUserEmail.send_email(client=client, maillisting=maillisting)


class SendUserEmail:
    """
    Utils class for sending the email for user.
    """
    _TEMPLATE = "emails/mailing_list.html"
    _SUBJECT = "The new client fulfilled the form."

    @classmethod
    def send_email(cls, client: Client, maillisting: Maillisting) -> None:
        """
        Function to send the email to the user.

        Args:
            client (Client) - django Cleint model
            emails (List[Maillisting]) - the list of Maillisting instances.
        """
        to_email = maillisting.email
        from_email = settings.EMAIL_HOST_USER
        subject = cls._SUBJECT
        year = cls._get_current_year()
        template_path = cls._TEMPLATE
        html_message = render_to_string(
            template_path,
            {
                'client_full_name': client.full_name,
                'client_email': client.email,
                'client_message': client.message,
                'year': year
            }
        )
        return send_email_from_html(subject, html_message, from_email, [to_email], html_message)

    @staticmethod
    def _get_current_year() -> str:
        """
        Get the string of current year.
        """
        now = timezone.now().date()
        return str(now.year)
