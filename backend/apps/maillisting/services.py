"""
The file contains the encapsulated business logic for maillisting application.
"""
from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from django.template.loader import render_to_string

from apps.clients.models import Client
from apps.clients.repository import ClientRepository
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
        from_email = settings.DEFAULT_FROM_EMAIL
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


class NewClientNotificationService:
    """
    Notifies the company inbox about a freshly submitted "Connect with us" form.

    Unlike MailListingService, the recipient is static: it does not depend on the
    Maillisting table, and the email is never sent to the client themselves.
    """
    _TEMPLATE = "emails/mailing_list.html"
    _SUBJECT = "The new client fulfilled the form."
    _RECIPIENTS = ["info@complexitysolution.com"]

    @classmethod
    def send_email(cls, client: Client) -> None:
        """
        Sends the notification about the new client to the static recipient list.

        Args:
            client (Client) - the newly created Client instance.
        """
        html_message = render_to_string(
            cls._TEMPLATE,
            {
                'client_full_name': client.full_name,
                'client_email': client.email,
                'client_message': client.message,
                'user_email': ", ".join(cls._RECIPIENTS),
                'year': str(timezone.now().year),
            }
        )
        send_email_from_html(
            cls._SUBJECT,
            html_message,
            settings.DEFAULT_FROM_EMAIL,
            cls._RECIPIENTS,
        )


class DailyClientsDigestService:
    """
    Builds and sends a single digest email listing every client that submitted
    the "Connect with us" form during the last 24 hours.

    Unlike MailListingService, which fires one email per client to the Maillisting
    recipients, this runs on a schedule and sends one email to a fixed address.
    """
    _TEMPLATE = "emails/daily_clients_digest.html"
    _SUBJECT = "New clients for the last 24 hours: {count}"
    _WINDOW = timedelta(days=1)

    @classmethod
    def send_digest(cls) -> int:
        """
        Collects the clients created within the last 24 hours and emails them as one digest.
        An empty period sends nothing.

        Return:
            The number of clients included in the digest (0 means no email was sent).
        """
        end = timezone.now()
        start = end - cls._WINDOW

        clients = list(ClientRepository.get_created_between(start=start, end=end))
        if not clients:
            return 0

        html_message = render_to_string(
            cls._TEMPLATE,
            {
                'clients': clients,
                'period_start': start,
                'period_end': end,
                'clients_count': len(clients),
                'year': str(end.year),
            }
        )
        send_email_from_html(
            cls._SUBJECT.format(count=len(clients)),
            html_message,
            settings.DEFAULT_FROM_EMAIL,
            settings.DAILY_DIGEST_RECIPIENTS,
        )
        return len(clients)
