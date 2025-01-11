"""
The file contains celery backgrounds tasks
"""
import logging
from typing import Dict

from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail, BadHeaderError
from django.utils.html import strip_tags

from config.celery import app


log = logging.getLogger(__name__)


@app.task(bind=True, max_retries=5, default_retry_delay=10)
def bg_send_email(
    self,
    params: Dict
) -> None:
    """
    Sends an email with the provided subject,
    message, and sender and recipient email addresses.
    """
    try:
        send_mail(
            params["subject"], params["message"],
            params["from_email"], params["recipient_list"]
        )
        log.info("Email successful sent.")
    except BadHeaderError as e:
        log.error("Error in email header: %s", e)
    except Exception as e:
        log.error("Error sending email: %s, retrying...", e)
        raise self.retry(exc=e)


@app.task(bind=True, max_retries=5, default_retry_delay=10)
def bg_send_email_from_html(
    self,
    params: Dict
) -> None:
    """
    Sends an email with HTML content.
    """
    try:
        # If no plain text content is provided, use a simple strip_tags as fallback
        text_content = params["text_content"]
        if not text_content:
            text_content = strip_tags(params["html_content"])

        # Create an instance of EmailMultiAlternatives
        msg = EmailMultiAlternatives(
            params["subject"], text_content,
            params["from_email"], params["recipient_list"]
        )
        msg.attach_alternative(params["html_content"], "text/html")  # Attach the HTML version
        msg.send()  # Send the email
        log.info("Email successful sent.")
    except Exception as e:
        log.error("Error sending email: %s, retrying...", e)
        raise self.retry(exc=e)
