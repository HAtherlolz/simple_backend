"""
The file contains celery background tasks related to the maillisting application.
"""
import logging

from config.celery import app

from .services import DailyClientsDigestService


log = logging.getLogger(__name__)


@app.task(bind=True, max_retries=3, default_retry_delay=300)
def send_daily_clients_digest(self) -> None:
    """
    Sends a single digest email with every client that filled the form
    during the last 24 hours. Scheduled by celery beat, see config/celery.py.
    """
    try:
        count = DailyClientsDigestService.send_digest()
    except Exception as e:
        log.error("Failed to build the daily clients digest: %s, retrying...", e)
        raise self.retry(exc=e)

    if not count:
        log.info("Daily clients digest skipped: no new clients for the last 24 hours.")
        return

    log.info("Daily clients digest queued for %s client(s).", count)
