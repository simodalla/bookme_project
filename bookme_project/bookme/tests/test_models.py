# -*- coding: iso-8859-1 -*-

import datetime

from django.test import TestCase
from django.utils import timezone

from .factories import UserFactory, BookOperatorsGroupFactory, AdminFactory
from ..models import (Calendar, BookingType, SlotTime, DailySlotTimePattern,
                      DAYS)


class FactoriesTest(TestCase):
    def test_auth(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        operators = BookOperatorsGroupFactory()
        UserFactory(groups=(operators,))


class CalendarSlotTimeCreationTest(TestCase):

    def setUp(self):
        self.calendar, created = Calendar.objects.get_or_create(
            name='Prenotazioni Servizi Anagrafici',
            defaults={'description': 'Calendario delle prenotazioni per '
                                     'servizi anagrafici',
                      'slot_length': 30})
        # print(Calendar.objects.all())

        for name in ['Permesso di Permesso Soggiorno', 'Pratica di residenza']:
            booking_type, created = BookingType.objects.get_or_create(
                calendar=self.calendar, name=name)

        self.dstps_data = [(DAYS.we, '9:00', '11:00'),
                           (DAYS.th, '10:00', '13:00'),
                           (DAYS.th, '14:00', '16:00'),
                           (DAYS.fr, '11:00', '13:00'), ]
        for day, start, end in self.dstps_data:
            dstp, created = DailySlotTimePattern.objects.get_or_create(
                calendar=self.calendar, day=day,
                start_time=start, end_time=end)

        self.start_date = datetime.date(2013, 5, 6)
        self.end_date = datetime.date(2013, 6, 22)

    def test_create_slot_times_method_wrong_parameter_type(self):
        # print(self.calendar.dailyslottimepattern_set.all())
        self.assertRaises(TypeError, self.calendar.create_slot_times, 'a', 'b')

    def test_create_slot_times_method_wrong_parameter_values(self):
        # print(self.calendar.dailyslottimepattern_set.all())
        self.assertRaises(ValueError, self.calendar.create_slot_times,
                          datetime.date.today() + datetime.timedelta(days=2),
                          datetime.date.today())
        self.assertRaises(ValueError, self.calendar.create_slot_times,
                          datetime.date.today(),
                          datetime.date.today() + datetime.timedelta(days=500))

    def test_create_slot_times_method_without_related_pattern(self):
        """
        Test that the call of method 'create_slot_times' on one Calendat
        without related DailySlotTimePattern raise a ValueError exception
        """
        self.calendar.dailyslottimepattern_set.all().delete()
        self.assertRaisesMessage(
            ValueError,
            "{} has no related {}".format(
                self.calendar, DailySlotTimePattern._meta.verbose_name_plural),
            self.calendar.create_slot_times,
            datetime.date.today(),
            datetime.date.today() + datetime.timedelta(days=40))

    def test_create_slot_times_method(self):
        self.calendar.create_slot_times(self.start_date, self.end_date)




