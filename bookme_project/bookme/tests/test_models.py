# -*- coding: iso-8859-1 -*-

from datetime import date, timedelta

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
        # 6 may of 2013 is a monday
        self.start_date = date(2013, 5, 6)

        for name in ['Permesso di Permesso Soggiorno', 'Pratica di residenza']:
            booking_type, created = BookingType.objects.get_or_create(
                calendar=self.calendar, name=name)

        self.dstps_data = [(DAYS.we, '9:00', '11:00'),
                           (DAYS.th, '10:00', '13:00'),
                           (DAYS.th, '14:00', '16:00'),
                           (DAYS.fr, '11:00', '13:00'), ]
        # for day, start, end in self.dstps_data:
        #     dstp, created = DailySlotTimePattern.objects.get_or_create(
        #         calendar=self.calendar, day=day,
        #         start_time=start, end_time=end)
        #self.end_date = date(2013, 6, 22)

    def tearDown(self):
        self.calendar.dailyslottimepattern_set.all().delete()

    def test_create_slot_times_method_wrong_parameter_type(self):
        # print(self.calendar.dailyslottimepattern_set.all())
        self.assertRaises(TypeError, self.calendar.create_slot_times, 'a', 'b')

    def test_create_slot_times_method_wrong_parameter_values(self):
        # print(self.calendar.dailyslottimepattern_set.all())
        self.assertRaises(ValueError, self.calendar.create_slot_times,
                          date.today() + timedelta(days=2),
                          date.today())
        self.assertRaises(ValueError, self.calendar.create_slot_times,
                          date.today(),
                          date.today() + timedelta(days=500))

    def test_create_slot_times_method_without_related_pattern(self):
        """
        Test that the call of method 'create_slot_times' on one Calendat
        without related DailySlotTimePattern raise a ValueError exception
        """
        self.calendar.dailyslottimepattern_set.all().delete()
        self.assertRaisesMessage(
            ValueError,
            "{} has no related DailySlotTimePattern objects".format(
                self.calendar),
            self.calendar.create_slot_times,
            date.today(),
            date.today() + timedelta(days=40))

    def test_create_slot_times_method_with_same_day_and_no_dstp(self):
        self.calendar.dailyslottimepattern_set.all().delete()
        self.calendar.slottime_set.all().delete()

        self.calendar.dailyslottimepattern_set.get_or_create(
            day=self.start_date.weekday() + 1, start_time='9:00',
            end_time='11:00')
        result = self.calendar.create_slot_times(self.start_date,
                                                 self.start_date)
        self.assertEqual(result, 0)
        self.assertEqual(self.calendar.slottime_set.count(), 0)

    def test_create_slot_times_method_with_same_day(self):
        self.calendar.dailyslottimepattern_set.all().delete()
        self.calendar.slottime_set.all().delete()

        self.calendar.dailyslottimepattern_set.get_or_create(
            day=self.start_date.weekday(), start_time='9:00',
            end_time='11:00')
        result = self.calendar.create_slot_times(self.start_date,
                                                 self.start_date)
        self.assertEqual(result, 4)
        self.assertEqual(self.calendar.slottime_set.count(), 4)

    def test_create_slot_times_method_with_same_day_two_dstp(self):
        self.calendar.dailyslottimepattern_set.all().delete()
        self.calendar.slottime_set.all().delete()

        self.calendar.dailyslottimepattern_set.get_or_create(
            day=self.start_date.weekday(), start_time='9:00',
            end_time='11:00')
        self.calendar.dailyslottimepattern_set.get_or_create(
            day=self.start_date.weekday() + 1, start_time='9:00',
            end_time='11:00')
        result = self.calendar.create_slot_times(self.start_date,
                                                 self.start_date)
        self.assertEqual(result, 4)
        self.assertEqual(self.calendar.slottime_set.count(), 4)




