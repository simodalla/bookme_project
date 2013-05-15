# -*- coding: iso-8859-1 -*-
import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices
from model_utils.models import TimeStampedModel, StatusField

from .core import get_range_days, get_week_map_by_weekday


DAYS = Choices((0, 'mo', _('monday')), (1, 'tu', _('tuesday')),
               (2, 'we', _('wednesday')), (3, 'th', _('thursday')),
               (4, 'fr', _('friday')), (5, 'sa', _('saturday')),
               (6, 'su', _('sunday')),)


class Calendar(TimeStampedModel):
    name = models.CharField(max_length=30, verbose_name=_('name'), unique=True)
    gid = models.CharField(max_length=300, verbose_name=_('google id'),
                           blank=True, null=True)
    description = models.TextField(blank=True, null=True, default='')
    slot_length = models.PositiveIntegerField(
        verbose_name=_('slot length'), default=30,
        help_text=_('default length in minutes of  slot time.'))

    objects = models.Manager()

    class Meta:
        verbose_name = _('calendar')
        verbose_name_plural = _('calendars')
        ordering = []

    def __unicode__(self):
        return '{} {}'.format(self.__class__.__name__, self.name)

    def create_slot_times(self, start_date, end_date):
        if self.dailyslottimepattern_set.count() == 0:
            raise ValueError("{} has no related {}".format(
                self, DailySlotTimePattern._meta.verbose_name_plural))
        try:
            days = get_week_map_by_weekday(
                get_range_days(start_date, end_date))
            # print(days)
        except Exception as e:
            raise e
        # dstpatterns = self.dailyslottimepattern_set.all()
        for pattern in self.dailyslottimepattern_set.all():
        # for weekday_ in set(dstpatterns.values_list(
        #         'day', flat=True)):
        #     print("{} - {}".format(pattern.day, days[str(pattern.day)]))
            for day in days[str(pattern.day)]:
                if day == datetime.date(2013, 5, 8):
                    print(day)
                    cache_start_datetime = datetime.datetime.combine(
                        day, pattern.start_time)
                    end_datetime = datetime.datetime.combine(
                        day, pattern.end_time)
                    while (((end_datetime - cache_start_datetime).seconds/60)
                               > self.slot_length):
                        print('{}--{}'.format(
                            cache_start_datetime,
                            cache_start_datetime + datetime.timedelta(
                                minutes=self.slot_length)))


            # print "****"
        # for
        print('debug')

class DailySlotTimePattern(models.Model):
    calendar = models.ForeignKey(Calendar)
    day = models.IntegerField(choices=DAYS, default=DAYS.mo,
                              verbose_name=_('day'))
    start_time = models.TimeField(verbose_name=_('start time'))
    end_time = models.TimeField(verbose_name=_('end time'))

    class Meta:
        verbose_name = _('daily slot time pattern')
        verbose_name_plural = _('daily slot time patterns')
        ordering = ['calendar']
        unique_together = ('calendar', 'day', 'start_time')

    def __unicode__(self):
        return '{} {} ({}-{})'.format(self.__class__.__name__,
                                      self.get_day_display(),
                                      self.start, self.end)


class BookingType(models.Model):
    calendar = models.ForeignKey(Calendar)
    name = models.CharField(max_length=30, verbose_name=_('name'))
    description = models.TextField(blank=True, null=True, default='')
    notes = models.TextField(blank=True, null=True, default='')

    class Meta:
        verbose_name = _('booking type')
        verbose_name_plural = _('booking types')
        unique_together = ('calendar', 'name')

    def __unicode__(self):
        pass


class SlotTime(models.Model):
    calendar = models.ForeignKey(Calendar)
    start = models.DateTimeField(verbose_name=_('start datetime'))
    end = models.DateTimeField(verbose_name=_('end datetime'))

    class Meta:
        verbose_name = 'slot time'
        verbose_name_plural = 'slot times'
        ordering = []

    def __unicode__(self):
        pass


class Booking(TimeStampedModel):
    STATUS = Choices(('free', _('free')), ('taken', _('taken')))
    nin = models.CharField(max_length=30, verbose_name=_('NIN'),
                           help_text=_('insert the National Identification'
                                       ' Number'))
    mobile = models.CharField(max_length=30, verbose_name=_('mobile number'))
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    type = models.ForeignKey(BookingType, blank=True, null=True)
    slot_time = models.OneToOneField(SlotTime, blank=True, null=True)
    status = StatusField()

    class Meta:
        verbose_name = _('booking')
        verbose_name_plural = _('bookings')
        ordering = []

    def __unicode__(self):
        return '{} id:{}'.format('Booking', self.pk)
