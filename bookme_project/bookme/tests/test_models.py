# -*- coding: iso-8859-1 -*-

from datetime import date, timedelta

from django.core.urlresolvers import reverse
from django.forms import ValidationError
from django.test import TestCase
from django.utils import timezone

from .factories import CalendarFactory
from ..models import (Calendar, BookingType, SlotTimesGeneration,
                      DailySlotTimePattern, DAYS)
from ..forms import SlotTimesGenerationForm


class SlotTimesGenerationModelTest(TestCase):

    def setUp(self):
        self.calendar = CalendarFactory()
        # 6 may of 2013 is a monday
        self.start_date = date(2013, 5, 6)

    def test_create_slot_times_method_with_wrong_start_and_end_date(self):
        slot_time_gen = SlotTimesGeneration.objects.create(
            calendar=self.calendar,
            start_date=date.today() + timedelta(days=2),
            end_date=date.today())
        self.assertRaises(ValueError, slot_time_gen.create_slot_times)
        slot_time_gen = SlotTimesGeneration.objects.create(
            calendar=self.calendar,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=500))
        self.assertRaises(ValueError, slot_time_gen.create_slot_times)

    def test_create_slot_times_method_without_related_pattern(self):
        """
        Test that the call of method 'create_slot_times' on one Calendar
        without related DailySlotTimePattern raise a ValueError exception
        """
        slot_time_gen = SlotTimesGeneration.objects.create(
            calendar=self.calendar,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=40))
        self.assertRaisesMessage(
            ValueError,
            "{} has no related DailySlotTimePattern objects".format(
                self.calendar),
            slot_time_gen.create_slot_times)

    def test_create_slot_times_method_with_same_day_and_no_dstp(self):
        """
        Test that the call of method 'create_slot_times' on SlotTimesGeneration
        with the same 'start_date' and 'end_date' fields. The same date
        'start_date' and 'end_date' is a weekday that not in
        DailySlotTimePattern day.
        """
        slot_time_gen = SlotTimesGeneration.objects.create(
            calendar=self.calendar,
            start_date=self.start_date,
            end_date=self.start_date)
        slot_time_gen.calendar.dailyslottimepattern_set.create(
            day=self.start_date.weekday() + 1, start_time='9:00',
            end_time='11:00')
        result = slot_time_gen.create_slot_times()
        self.assertEqual(result, 0)
        self.assertEqual(slot_time_gen.calendar.slottime_set.count(), 0)

    def test_create_slot_times_method_with_same_day(self):
        slot_time_gen = SlotTimesGeneration.objects.create(
            calendar=self.calendar,
            start_date=self.start_date,
            end_date=self.start_date)
        slot_time_gen.calendar.dailyslottimepattern_set.create(
            day=self.start_date.weekday(), start_time='9:00',
            end_time='11:00')
        result = slot_time_gen.create_slot_times()
        self.assertEqual(result, 4)
        self.assertEqual(slot_time_gen.calendar.slottime_set.count(), 4)

    def test_create_slot_times_method_with_same_day_two_dstp(self):
        slot_time_gen = SlotTimesGeneration.objects.create(
            calendar=self.calendar,
            start_date=self.start_date,
            end_date=self.start_date)
        slot_time_gen.calendar.dailyslottimepattern_set.create(
            day=self.start_date.weekday(), start_time='9:00',
            end_time='11:00')
        self.calendar.dailyslottimepattern_set.get_or_create(
            day=self.start_date.weekday() + 1, start_time='9:00',
            end_time='11:00')
        result = slot_time_gen.create_slot_times()
        self.assertEqual(result, 4)
        self.assertEqual(self.calendar.slottime_set.count(), 4)


class SlotTimesGenerationFormTest(TestCase):

    def setUp(self):
        self.start_date = date(2013, 5, 6)

    def test_form_custom_errors_validation(self):
        calendar = CalendarFactory()
        data = {'calendar': calendar.pk,
                'start_date': self.start_date,
                'end_date': self.start_date - timedelta(days=1)}
        form = SlotTimesGenerationForm(data)
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError, form.clean)

    def test_form_correct_validation(self):
        calendar = CalendarFactory()
        data = {'calendar': calendar.pk,
                'start_date': self.start_date,
                'end_date': self.start_date - timedelta(days=1)}
        form = SlotTimesGenerationForm(data)
        self.assertFalse(form.is_valid())




