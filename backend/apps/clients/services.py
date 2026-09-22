"""
The file contains encapsulated business logic related to Client model.
"""
from typing import Dict, Tuple, Optional

from apps.maillisting.services import NewClientNotificationService

from .models import Client
from .repository import ClientRepository


class ClientService:
    """
    The service class to manage client model.
    """

    _repo = ClientRepository

    @classmethod
    def create_client(cls, data: Dict) -> Tuple[Optional[Client], Optional[str]]:
        """
        Creates the client instance and notifies the company inbox about it.
        """
        client, err = cls._repo.create(data=data)
        if err:
            return None, err

        NewClientNotificationService.send_email(client=client)
        return client, None
