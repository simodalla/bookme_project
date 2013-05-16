# -*- coding: iso-8859-1 -*-

from datetime import datetime, timedelta

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
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
        try:
            days = get_week_map_by_weekday(
                get_range_days(start_date, end_date))
        except Exception as e:
            raise e
        if self.dailyslottimepattern_set.count() == 0:
            raise ValueError("{} has no related DailySlotTimePattern "
                             "objects".format(self))
        count = 0
        for pattern in self.dailyslottimepattern_set.all():
            for day in days[str(pattern.day)]:
                cache_start_datetime = datetime.combine(day, pattern.start_time)
                end_datetime = datetime.combine(day, pattern.end_time)
                while (((end_datetime - cache_start_datetime).seconds/60)
                        >= self.slot_length):
                    start_slot = cache_start_datetime
                    end_slot = cache_start_datetime + timedelta(
                        minutes=self.slot_length)
                    slot, created = self.slottime_set.get_or_create(
                        day=day,
                        start_time=start_slot.strftime('%H:%M'),
                        end_time=end_slot.strftime('%H:%M'))
                    if created:
                        count += 1
                    # print('{}--{}'.format(start_slot, end_slot))
                    cache_start_datetime = end_slot
        return count

    def daily_slot_time_patterns(self):
        return '<br >'.join(
            ['<b>{}</b>: {} - {}'.format(dstp.get_day_display(),
                                         dstp.start_time, dstp.end_time)
             for dstp in self.dailyslottimepattern_set.order_by('day')])
    daily_slot_time_patterns.short_description = _('daily slot time patterns')
    daily_slot_time_patterns.allow_tags = True

    def booking_types(self):
        return '<br >'.join(
            ['<a href="{}">{}</a>'.format(
                reverse('admin:bookme_bookingtype_change', args=(bt.pk,)),
                bt.name) for bt in self.bookingtype_set.all()])
    booking_types.short_description = _('booking types')
    booking_types.allow_tags = True


class DailySlotTimePattern(TimeStampedModel):
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
                                      self.start_time, self.end_time)


class BookingType(models.Model):
    calendar = models.ForeignKey(Calendar)
    name = models.CharField(max_length=30, verbose_name=_('name'))
    description = models.TextField(blank=True, null=True, default='')
    notes = models.TextField(blank=True, null=True, default='')

    class Meta:
        ordering = ['calendar', 'name']
        verbose_name = _('booking type')
        verbose_name_plural = _('booking types')
        unique_together = ('calendar', 'name')

    def __unicode__(self):
        return self.name


class SlotTimesGeneration(TimeStampedModel):
    calendar = models.ForeignKey(Calendar)
    start_date = models.DateField(verbose_name=_('start date'))
    end_date = models.DateField(verbose_name=_('end date'))

    class Meta:
        ordering = ['calendar', 'start_date', 'end_date']
        verbose_name = _('slot times creation')
        verbose_name_plural = _('slot times creations')
        unique_together = ('calendar', 'start_date', 'end_date')


class SlotTime(TimeStampedModel):
    STATUS = Choices(('free', _('free')), ('taken', _('taken')))
    calendar = models.ForeignKey(Calendar)
    day = models.DateField(verbose_name=_('day'))
    start_time = models.TimeField(verbose_name=_('start time'))
    end_time = models.TimeField(verbose_name=_('end time'))
    status = StatusField(default=STATUS.free)
    generation = models.ForeignKey(SlotTimesGeneration, blank=True, null=True)

    class Meta:
        verbose_name = 'slot time'
        verbose_name_plural = 'slot times'
        ordering = []

    def __unicode__(self):
        result = '{} {}:{}'.format(self.day, self.start_time, self.end_time)
        return result


class Booking(TimeStampedModel):
    nin = models.CharField(max_length=30, verbose_name=_('NIN'),
                           help_text=_('insert the National Identification'
                                       ' Number'))
    mobile = models.CharField(max_length=30, verbose_name=_('mobile number'))
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    type = models.ForeignKey(BookingType, blank=True, null=True)
    slot_time = models.OneToOneField(SlotTime, blank=True, null=True)

    class Meta:
        verbose_name = _('booking')
        verbose_name_plural = _('bookings')
        ordering = []

    def __unicode__(self):
        return '{} id:{}'.format('Booking', self.pk)
