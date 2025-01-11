"""
The file contains the db queries for Maillisting model.
"""
from apps.core.utils import BaseRepository

from .models import Maillisting


class MaillistingRepository(BaseRepository):
    """
    The repository class that provides method for managing db queries.
    """

    _model = Maillisting
