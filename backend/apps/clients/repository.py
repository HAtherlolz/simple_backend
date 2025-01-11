"""
The file contains the db queries related with Client model.
"""
from apps.core.utils import BaseRepository

from .models import Client


class ClientRepository(BaseRepository):
    """
    The repository class that provides method for managing db queries.
    """

    _model = Client
