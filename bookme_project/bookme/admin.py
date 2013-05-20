# -*- coding: iso-8859-1 -*-

from django.contrib import admin

from .models import (BookingType, Calendar, DailySlotTimePattern, SlotTime,
                     SlotTimesGeneration)
from .forms import SlotTimesGenerationForm


class BookingTypeInline(admin.TabularInline):
    extra = 1
    model = BookingType
    ordering = ['calendar', 'name']


class DailySlotTimePatternInline(admin.TabularInline):
    extra = 1
    model = DailySlotTimePattern
    ordering = ['day', 'start_time', 'end_time']


class BookingTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'calendar', 'description', 'notes']
    list_per_page = 20


class CalendarAdmin(admin.ModelAdmin):
    list_display = ['name', 'gid', 'slot_length', 'booking_types',
                    'daily_slot_time_patterns']
    list_per_page = 20
    inlines = [BookingTypeInline, DailySlotTimePatternInline]

    class Media:
        css = {'all': ('bookme/admin/css/custom.css',)}


class SlotTimesGenerationAdmin(admin.ModelAdmin):
    form = SlotTimesGenerationForm
    list_display = ['pk', 'calendar', 'created', 'start_date', 'end_date']
    list_filter = ['calendar']
    list_per_page = 20
    ordering = ['calendar', 'created', 'start_date', 'end_date']


class SlotTimeAdmin(admin.ModelAdmin):
    list_display = ['pk', 'calendar', 'day', 'start_time', 'end_time', 'status']
    list_filter = ['calendar']
    list_per_page = 20
    ordering = ['calendar', 'day', 'start_time', 'end_time']


admin.site.register(BookingType, BookingTypeAdmin)
admin.site.register(Calendar, CalendarAdmin)
admin.site.register(SlotTimesGeneration, SlotTimesGenerationAdmin)
admin.site.register(SlotTime, SlotTimeAdmin)
