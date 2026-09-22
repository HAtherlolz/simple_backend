"""
The file contains the db queries related with Client model.
"""
from datetime import datetime
from typing import List

from apps.core.utils import BaseRepository

from .models import Client


class ClientRepository(BaseRepository):
    """
    The repository class that provides method for managing db queries.
    """

    _model = Client

    @classmethod
    def get_created_between(cls, start: datetime, end: datetime) -> List[Client]:
        """
        Retrieves the clients created within the [start, end) time window, oldest first.

        Args:
            start (datetime): timezone-aware lower bound, inclusive.
            end (datetime): timezone-aware upper bound, exclusive.
        """
        return cls._model.objects.filter(
            created_at__gte=start,
            created_at__lt=end
        ).order_by('created_at')
