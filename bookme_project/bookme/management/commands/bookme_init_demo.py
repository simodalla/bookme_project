# -*- coding: iso-8859-1 -*-

from django.core.management.base import BaseCommand, CommandError

from ...models import Calendar, BookingType, DailySlotTimePattern, DAYS


class Command(BaseCommand):
    help = 'Create initial data e make initializations'

    def handle(self, *args, **options):

        calendar, created = Calendar.objects.get_or_create(
            name='Prenotazioni Servizi Anagrafici',
            defaults={'description': 'Calendario delle prenotazioni per '
                                     'servizi anagrafici',
                      'slot_length': 30})

        for name in ['Permesso di Permesso Soggiorno', 'Pratica di residenza']:
            booking_type, created = BookingType.objects.get_or_create(
                calendar=calendar, name=name)

        dstps_data = [(DAYS.we, '9:00', '11:00'),
                      (DAYS.th, '10:00', '13:00'),
                      (DAYS.th, '14:00', '16:00'),
                      (DAYS.fr, '11:00', '13:00'), ]
        for day, start, end in dstps_data:
            dstp, created = DailySlotTimePattern.objects.get_or_create(
                calendar=calendar, day=day, start=start, end=end)





