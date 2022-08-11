from django.contrib import admin
from .models import PrayerTiming
# Register your models here.
@admin.register(PrayerTiming)
class PrayerTimingAdmin(admin.ModelAdmin):
    list_display = ('fajr', 'dhuhr', 'asr', 'maghrib', 'isha', )
