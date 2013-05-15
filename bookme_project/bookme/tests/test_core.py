# -*- coding: iso-8859-1 -*-

import datetime
from django.test import TestCase

from ..core import get_range_days, get_week_map_by_weekday


class GetRangeDaysTest(TestCase):

    def setUp(self):
        self.start_date = datetime.date(2013, 5, 6)
        self.end_date = datetime.date(2013, 6, 22)

    def test_create_slot_times_method_wrong_parameter_type(self):
        self.assertRaises(TypeError, get_range_days, 'a', 'b')

    def test_create_slot_times_method_wrong_parameter_values(self):
        self.assertRaises(ValueError, get_range_days,
                          datetime.date.today() + datetime.timedelta(days=2),
                          datetime.date.today())
        self.assertRaises(ValueError, get_range_days,
                          datetime.date.today(),
                          datetime.date.today() + datetime.timedelta(days=500))

    def test_create_slot_times_call(self):
        days = get_range_days(self.start_date,
                              self.end_date)


class GetWeekMapByWeekdayTest(TestCase):

    def setUp(self):
        self.start_date = datetime.date(2013, 5, 6)
        self.end_date = datetime.date(2013, 6, 22)

    def test_get_week_map_by_weekday_method_wrong_parameter_type(self):
        self.assertRaises(ValueError, get_week_map_by_weekday, 777)

    def test_get_week_map_by_weekday_call(self):
        result = get_week_map_by_weekday(get_range_days(self.start_date,
                                                        self.end_date))