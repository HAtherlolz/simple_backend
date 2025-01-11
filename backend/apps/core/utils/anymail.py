"""
This module provides functions to send emails using Django's email utilities.
 It includes both plain text and HTML email sending capabilities,
 encapsulating the functionality within a simplified API for ease of use in Django projects.

Functions:
- send_email: Sends a simple plain text email.
- send_email_from_html: Sends an email with HTML content,
 optionally including a plain text version for email clients that do not support HTML.

Both functions aim to abstract the complexities of sending emails with Django,
 handling errors gracefully and providing a clear interface for developers.
 The module demonstrates how to use Django's built-in `send_mail` and `EmailMultiAlternatives`
 for email sending tasks, catering to a wide range of email content types.

Example Usage:
    from email_sending_module import send_email, send_email_from_html

    # Sending a plain text email
    send_email("Test Subject", "This is the body of the email.", "from@example.com", ["to@example.com"])

    # Sending an HTML email with a fallback plain text version
    send_email_from_html(
    "Test Subject", "<html><body><h1>HTML Content</h1></body></html>", "from@example.com", ["to@example.com"]
    )

Note:
- These functions are designed for use within Django projects
 and require Django's EMAIL_BACKEND to be properly configured.
- Error handling is implemented to catch and respond to common issues such as bad header errors.
"""
from dataclasses import asdict
from typing import Dict

from django.template.loader import render_to_string

from ..enums import EmailParams, EmailHTMLParams
from ..tasks import bg_send_email, bg_send_email_from_html


def send_email(subject, message, from_email, recipient_list):
    """Sends an email with the provided subject, message, and sender and recipient email addresses.

    Parameters:
        subject (str): The subject of the email.
        message (str): The content of the email.
        from_email (str): The sender's email address.
        recipient_list (list[str]): A list of recipient email addresses.

    Returns:
        HttpResponse: indicating whether the email was sent successfully
         or an error occurred during the process.
    """
    params = EmailParams(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list
    )
    bg_send_email.delay(asdict(params))


def send_email_from_html(subject, html_content, from_email, recipient_list, text_content=None):
    """
    Send an email with HTML content.

    Parameters:
    - subject (str): The subject of the email.
    - html_content (str): The HTML content of the email.
    - from_email (str): The sender's email address.
    - recipient_list (list): A list of recipient email addresses.
    - text_content (str, optional): The plain text content of the email.
     If not provided, a simple 'strip_tags' conversion of the HTML content will be used as fallback.

    Returns:
    - HttpResponse: A response indicating the result of the email sending.

    Example usage:
    send_email_from_html(
    "Hello", "<html><body><h1>Welcome</h1></body></html>", "sender@example.com", ["recipient@example.com"]
    )

    Note: This method requires the 'django.utils.html' module to be imported.

    """
    params = EmailHTMLParams(
        subject=subject,
        html_content=html_content,
        from_email=from_email,
        recipient_list=recipient_list,
        text_content=text_content
    )
    bg_send_email_from_html.delay(asdict(params))


def html_to_message(template_path: str, variables: Dict) -> str:
    """
    Render the html with variables to string message
    """
    return render_to_string(
        template_path,
        variables
    )
