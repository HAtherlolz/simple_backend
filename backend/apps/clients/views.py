"""
The file contains APIView for handling
requests related to chili piper service.
"""
from rest_framework import status, permissions, generics
from rest_framework.response import Response

from apps.core.utils import error_response

from .services import ClientService
from .serializers import CreateClientSerializer
from .exceptions import (
    ClientErrorMessages,
    ClientSuccessMessages

)


class CreateClientAPIView(generics.CreateAPIView):
    """
    API View to handle GET requests for creating the client.
    """
    serializer_class = CreateClientSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        """
        API View to handle POST requests for creating the client instance.
        """
        serializer = self.get_serializer(data=self.request.data)
        if not serializer.is_valid():
            return error_response(detail=serializer.errors, status_code=400)

        _, err = ClientService.create_client(data=serializer.validated_data)
        if err:
            return error_response(detail=ClientErrorMessages.COULD_NOT_CREATE_CLIENT, status_code=400)

        return Response(
            {"detail": ClientSuccessMessages.CLIENT_SUCCESSFUL_CREATED},
            status=status.HTTP_200_OK
        )
