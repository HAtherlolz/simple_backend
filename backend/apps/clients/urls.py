"""
URL mapping for the user API.
"""
from django.urls import path

from .views import CreateClientAPIView


app_name = 'client'  # pylint: disable=invalid-name

urlpatterns = [
    path('create/', CreateClientAPIView.as_view(), name='create_client'),
]
