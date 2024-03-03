import os

import django
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from datacenter.models import Passcard, Visit  # noqa: E402
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


if __name__ == '__main__':
    active_passcards = Passcard.objects.filter(is_active=True)
    some_visitor = active_passcards[0].owner_name
    passcard_visits = Visit.objects.filter(passcard__owner_name=some_visitor)
    print(passcard_visits)
    for dangerous_visit in passcard_visits:
        if is_visit_long(dangerous_visit) is True:
            print(dangerous_visit)
    non_closed_visits = Visit.objects.filter(leaved_at=None)
    for visit in non_closed_visits:
        owner_name = visit.passcard.owner_name
        entry_time = localtime(visit.entered_at)
        print(f'{owner_name} зашёл в хранилище, время по Москве: {entry_time}')
        print(f'{owner_name} находится в хранилище: {get_duration(visit)}')
    count_active_passcard = len(Passcard.objects.filter(is_active=True))
    print('Количество активных пропусков:', count_active_passcard)
    print('Всего пропусков:', Passcard.objects.count())  # noqa: T001
