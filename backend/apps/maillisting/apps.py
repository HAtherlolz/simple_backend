"""
APP Config for user application.
"""
from django.apps import AppConfig


class MaillistingConfig(AppConfig):
    """
    MaillistingConfig class

    This class represents the configuration for the maillisting app in a Django project.

    Attributes:
    default_auto_field (str): The default auto field to use for models in the maillisting app.
    name (str): The name of the maillisting app.

    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.maillisting'
