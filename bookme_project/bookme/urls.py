# -*- coding: iso-8859-1 -*-

from django.conf.urls import patterns, url

from .views import HomeView, BookingTypeListView

urlpatterns = patterns(
    'bookme.views',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^bookingtypes/$', BookingTypeListView.as_view(),
        name='bookingtype_list'),
    url(r'^slottime/add/$', 'slottime_add', name='slottime_add'),
)
