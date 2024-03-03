import time
from django.utils.timezone import localtime, now


def get_duration(visit):
    entry_time = localtime(visit.entered_at)
    exit_time = localtime(visit.leaved_at)
    delta = exit_time - entry_time if exit_time else now()
    total_seconds = delta.total_seconds()
    return total_seconds


def is_visit_long(visit, minutes=60):
    duration_in_seconds = get_duration(visit)
    duration_in_minutes = round(duration_in_seconds / 60)
    return duration_in_minutes > minutes


def format_duration(duration):
    return time.strftime("%H:%M:%S", time.gmtime(duration))
