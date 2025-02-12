"""
Celery - Distributed Task Queue
"""

# pylint: disable=W0613 C0116 C0103

import os

from celery import Celery
from celery.schedules import crontab
from django.core.mail import EmailMessage

# set the default Django settings module for the 'celery' program.
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    f'{os.getenv("DJANGO_PROJECT_NAME")}.settings',
)

app = Celery(os.getenv("DJANGO_PROJECT_NAME"))
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Scheduling expired notifications and subscriptions processing
app.conf.beat_schedule = {
    # "process_expired_orders": {
    #     "task": "payment.tasks.process_expired_orders",
    #     "schedule": crontab(minute=0, hour=0),  # Execute daily at midnight.
    # },
}


@app.task(bind=True)
def send_verification_email(
    self,
    from_email,
    to,
    subject,
    body,
):
    """Celery app task for sending emails."""
    EmailMessage(
        from_email=from_email,
        to=to,
        subject=subject,
        body=body,
    ).send(fail_silently=False)
