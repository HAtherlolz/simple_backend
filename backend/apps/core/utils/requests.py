"""
The file contains the encapsulated logic of requests.
"""
import logging
from typing import Dict, Tuple, Any, Optional

import requests

from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type


log = logging.getLogger(__name__)


class RequestService:
    """
    The class contains the methods for managing requests.
    """

    @staticmethod
    def _process_response(response) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Helper method to process the response.

        Return:
            Success - Dict of response and None as error
            Failed - None and string of error
        """
        if response.status_code == 200:
            try:
                return response.json(), None
            except ValueError:
                log.error("Invalid JSON response: %s", response.text)
                return None, response.text
        else:
            log.error(
                "Error Response: status_code - %s, response - %s",
                response.status_code, response.text
            )
            return None, response.text

    @classmethod
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(2),
        retry=retry_if_exception_type(requests.RequestException)
    )
    def post(
            cls,
            url: str,
            payload: Dict,
            headers: Dict,
    ) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        The method for managing request and process the response.

        Return:
            Success - Dict of response and None as error
            Failed - None and string of error
        """
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        return cls._process_response(response=response)

    @classmethod
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(2),
        retry=retry_if_exception_type(requests.RequestException)
    )
    def post_form_data(
            cls,
            url: str,
            payload: Dict,
            headers: Dict,
    ) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        The method for managing request and process the response.

        Return:
            Success - Dict of response and None as error
            Failed - None and string of error
        """
        headers.pop("Content-Type", None)
        response = requests.post(url, headers=headers, files=payload, timeout=10)
        return cls._process_response(response=response)

    @classmethod
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(2),
        retry=retry_if_exception_type(requests.RequestException)
    )
    def get(
            cls,
            url: str,
            headers: Optional[Dict] = None
    ) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        The method for managing request and process the response.

        Return:
            Success - Dict of response and None as error
            Failed - None and string of error
        """
        if not headers:
            headers = {}

        response = requests.get(url, headers=headers, timeout=10)
        return cls._process_response(response=response)
