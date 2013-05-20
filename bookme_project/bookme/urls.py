# -*- coding: iso-8859-1 -*-

from django.conf.urls import patterns, url

from .views import HomeView

urlpatterns = patterns(
    'bookme.views',
    url(r'^$', HomeView.as_view(), name='home'),
)
