# -*- coding: iso-8859-1 -*-

from django.contrib import admin

from .models import Calendar, DailySlotTimePattern


class DailySlotTimePatternInline(admin.TabularInline):
    model = DailySlotTimePattern


class CalendarAdmin(admin.ModelAdmin):
    list_display = ['name', 'gid', 'slot_length']
    list_per_page = 20
    inlines = [DailySlotTimePatternInline]


admin.site.register(Calendar, CalendarAdmin)
