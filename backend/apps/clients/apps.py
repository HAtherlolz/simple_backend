"""
APP Config for user application.
"""
from django.apps import AppConfig


class ClientsConfig(AppConfig):
    """
    ClientsConfig class

    This class represents the configuration for the clients app in a Django project.

    Attributes:
    default_auto_field (str): The default auto field to use for models in the clients app.
    name (str): The name of the clients app.

    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.clients'
