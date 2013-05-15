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