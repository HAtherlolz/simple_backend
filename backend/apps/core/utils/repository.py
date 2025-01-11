"""
The file contains repository base class for managing queries to db.
"""
from typing import Optional, Tuple, Dict, List, Type

from django.db import models

from apps.core.utils import handle_exceptions


class BaseRepository:
    """
    Base repository class for handling common and frequently used queries
    related to the Django model.
    """
    _model: Type[models.Model] = None  # Ensures `_model` is a subclass of `models.Model`

    @classmethod
    def get_all(cls) -> List[models.Model]:
        """
        Retrieves the models instance by ID field.

        Return:
            success - Model instance and None of error
            failed - None of model instance and error string
        """
        return cls._model.objects.all()

    @classmethod
    @handle_exceptions(default_return=(None, "The instance with this ID does not exist."))
    def get_instance_by_id(
            cls,
            instance_id: str
    ) -> Tuple[Optional[models.Model], Optional[str]]:
        """
        Retrieves the models instance by ID field.

        Return:
            success - Model instance and None of error
            failed - None of model instance and error string
        """
        return cls._model.objects.get(id=instance_id), None

    @classmethod
    @handle_exceptions(default_return=(None, "Failed to update the instance."))
    def update(
            cls,
            instance: models.Model,
            data: Dict
    ) -> Tuple[Optional[models.Model], Optional[str]]:
        """
        Update the model instance with provided data.
        """
        for field, value in data.items():
            if hasattr(instance, field):
                setattr(instance, field, value)

        instance.save()
        return instance, None

    @classmethod
    @handle_exceptions(default_return=(None, "Failed to create an instance."))
    def create(cls, data: Dict) -> Tuple[Optional[models.Model], Optional[str]]:
        """
        Create the model instance with provided data.
        """
        instance = cls._model.objects.create(**data)
        return instance, None

    @classmethod
    def delete(cls, instance: models.Model) -> Optional[str]:
        """
        Delete the model instance by ID.
        """
        try:
            instance.delete()
        except Exception as e:
            return str(e)
        return None
