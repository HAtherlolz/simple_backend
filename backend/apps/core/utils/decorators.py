"""
The file contains decorators
"""
import logging
from functools import wraps
from typing import Tuple, Any, Callable, Optional

from django.db import transaction, DatabaseError


log = logging.getLogger(__name__)


def handle_exceptions(
        default_return: Tuple[Any, str] = (None, "An error occurred")
):
    """
    Decorator to handle exceptions and return a default response.

    Args:
        default_return (tuple): The default return value if an exception is raised.
    Returns:
        The decorated function's return value or the default response on exception.
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                log.error("handle_exceptions: %s", e)
                return default_return[0], default_return[1] if default_return[1] else str(e)
        return wrapper
    return decorator


def handle_transaction(func: Callable):
    """
    Decorator to wrap a method with a database transaction.

    Args:
        func (callable): The method to be wrapped in a transaction.

    Returns:
        callable: The wrapped method.
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Tuple[Optional[Any], Optional[str]]:
        try:
            with transaction.atomic():
                return func(*args, **kwargs)
        except DatabaseError as e:
            log.error("Database error during transaction in %s: %s", func.__name__, str(e))
            return None, str(e)
        except Exception as e:
            log.error("Unexpected error in %s: %s", func.__name__, str(e))
            return None, str(e)
    return wrapper
