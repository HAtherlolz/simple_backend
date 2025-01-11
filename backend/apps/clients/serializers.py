"""
The file contains serializers for serializing and representing content.
"""
from rest_framework import serializers

from .models import Client


class CreateClientSerializer(serializers.ModelSerializer):
    """
    The serializer class for serializing and validation
    the incoming data for client instance creation.
    """

    class Meta:
        """
        model (Model): The Django model associated with this serializer.
        fields (list): A list of fields to include in the serialized representation.
        """
        model = Client
        fields = "__all__"
        read_only_fields = ("created_at", "id")
