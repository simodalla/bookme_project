# -*- coding: iso-8859-1 -*-

import factory

from django.contrib.auth.models import User, Permission, Group

from .. import models

DOMAIN = 'comune.zolapredosa.bo.it'


class BookOperatorsGroupFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Group

    name = 'bookme_operators'

    @classmethod
    def _prepare(cls, create, **kwargs):
        group = super(BookOperatorsGroupFactory, cls)._prepare(create, **kwargs)
        group.permissions.add(
            *Permission.objects.filter(content_type__app_label='bookme'))
        return group


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User

    username = factory.Sequence(lambda n: 'user_%s' % n)
    password = factory.Sequence(lambda n: 'user_%s' % n)
    email = factory.LazyAttribute(lambda o: '{}@{}'.format(o.username, DOMAIN))
    is_staff = True
    is_active = True

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop('password', None)
        user = super(UserFactory, cls)._prepare(create, **kwargs)
        if password:
            user.set_password(password)
            if create:
                user.save()
        return user

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for group in extracted:
                self.groups.add(group)


class AdminFactory(UserFactory):
    FACTORY_FOR = User

    username = 'admin'
    password = 'admin'
    email = 'admin@{}'.format(DOMAIN)
    is_superuser = True


class DailySlotTimePatternFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.DailySlotTimePattern
    FACTORY_DJANGO_GET_OR_CREATE = ('calendar', 'day', 'start_time')


class BookingTypeFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.BookingType
    FACTORY_DJANGO_GET_OR_CREATE = ('calendar', 'name')

    name = factory.Sequence(lambda n: 'booking type {}'.format(n))


class CalendarFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.Calendar
    FACTORY_DJANGO_GET_OR_CREATE = ('name',)

    name = 'simple demo calendar'
    description = factory.LazyAttribute(
        lambda obj: 'description of {}'.format(obj.name))
    slot_length = 30

    bookingtype_1 = factory.RelatedFactory(BookingTypeFactory, 'calendar')
    bookingtype_2 = factory.RelatedFactory(BookingTypeFactory, 'calendar')


class CalendarPatternsFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.Calendar
    FACTORY_DJANGO_GET_OR_CREATE = ('name',)

    name = 'demo calendar with pattern'
    description = factory.LazyAttribute(
        lambda obj: 'description of {}'.format(obj.name))
    slot_length = 30

    dailyslottimepattern_1 = factory.RelatedFactory(
        DailySlotTimePatternFactory, 'calendar', day=models.DAYS.we,
        start_time='9:00', end_time='11:00')
    dailyslottimepattern_2 = factory.RelatedFactory(
        DailySlotTimePatternFactory, 'calendar', day=models.DAYS.th,
        start_time='10:00', end_time='13:00')
    dailyslottimepattern_3 = factory.RelatedFactory(
        DailySlotTimePatternFactory, 'calendar', day=models.DAYS.th,
        start_time='14:00', end_time='16:00')
    dailyslottimepattern_4 = factory.RelatedFactory(
        DailySlotTimePatternFactory, 'calendar', day=models.DAYS.fr,
        start_time='11:00', end_time='13:00')

    bookingtype_1 = factory.RelatedFactory(BookingTypeFactory, 'calendar')
    bookingtype_2 = factory.RelatedFactory(BookingTypeFactory, 'calendar')