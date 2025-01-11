"""
The file contains functions for DRF response.
"""
from rest_framework.response import Response


def error_response(detail: str, status_code: int) -> Response:
    """
    Creates a standardized error response for API endpoints.
    """
    return Response({"detail": detail}, status=status_code)
