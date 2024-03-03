import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from datacenter.models import Passcard, Visit  # noqa: E402
from django.utils.timezone import localtime
from datacenter.temporary_functions import is_visit_long, get_duration

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
