"""
The file contains the base implementation of cache service
"""
import logging
from typing import Optional, Any

from django.core.cache import cache


log = logging.getLogger(__name__)


class BaseCacheService:
    """
    Base class for cache services, providing methods to set, get,
    and delete cached data.
    """

    _action: str = "default_cache"

    @classmethod
    def _get_prefix(cls) -> str:
        """
        Get unique prefix for saving cache.
        Should be overridden in child classes for custom prefixes.
        """
        return cls._action

    @classmethod
    def set(cls, data: Any, timeout: int) -> None:
        """
        Set cache with a unique prefix and a timeout.

        Args:
            data: The data to cache.
            timeout: Time-to-live (TTL) for the cache in seconds.
        """
        prefix = cls._get_prefix()
        cache.set(prefix, data, timeout)

    @classmethod
    def get(cls) -> Optional[str]:
        """
        Retrieve cached data using the unique prefix.

        Returns:
            The cached data if it exists, otherwise None.
        """
        try:
            prefix = cls._get_prefix()
            return cache.get(prefix)
        except Exception as e:
            log.error("Failed to fetch cached data for prefix '%s': %s", cls._get_prefix(), e)
            return None

    @classmethod
    def delete(cls) -> None:
        """
        Delete cached data using the unique prefix.
        """
        prefix = cls._get_prefix()
        cache.delete(prefix)
