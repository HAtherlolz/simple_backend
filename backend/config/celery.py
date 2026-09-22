"""
Celery application setup and the beat schedule for periodic tasks.
"""
from __future__ import absolute_import
import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")


app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


# CELERY BEAT TASKS
app.conf.beat_schedule = {
    "send-daily-clients-digest": {
        "task": "apps.maillisting.tasks.send_daily_clients_digest",
        # 21:00 UTC == 00:00 Europe/Kyiv, so the digest covers the finished Kyiv day.
        "schedule": crontab(hour=21, minute=0),
    }
}
