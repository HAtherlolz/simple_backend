from __future__ import absolute_import
import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")


app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


# CELERY BEAT TASKS # TODO: uncomment when start to use cron tasks. # pylint: disable=fixme
# app.conf.beat_schedule = {
#     "check-event-notification-every-minute": {
#         "task": "apps.event.tasks.create_event_notification",
#         "schedule": crontab(),  # each minute
#     }
# }
