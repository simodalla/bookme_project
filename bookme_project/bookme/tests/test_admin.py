# -*- coding: iso-8859-1 -*-

from datetime import date, timedelta

from django.core.urlresolvers import reverse
from django.test import TestCase

from .factories import AdminFactory, CalendarFactory


class SlotTimesGenerationAdminTest(TestCase):

    def setUp(self):
        self.admin = AdminFactory()
        self.client.login(username=self.admin.username,
                          password=self.admin.username)
        self.start_date = date(2013, 5, 6)

    def test_add_view_form_validation(self):
        calendar = CalendarFactory()
        response = self.client.post(
            reverse('admin:bookme_slottimesgeneration_add'),
            data={'calendar': calendar.pk,
                  'start_date': self.start_date,
                  'end_date': self.start_date - timedelta(days=1)})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['errors']), 1)
