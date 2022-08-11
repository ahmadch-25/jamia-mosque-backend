from django.db import models
from django.forms import TimeInput


class PrayerTiming(models.Model):
    fajr = models.TimeField(auto_now=False, auto_now_add=False, verbose_name='Fajr Time', null=True)
    dhuhr = models.TimeField(auto_now=False, auto_now_add=False, verbose_name='Dhuhr Time', null=True)
    asr = models.TimeField(auto_now=False, auto_now_add=False, verbose_name='Asr Time', null=True)
    maghrib = models.TimeField(auto_now=False, auto_now_add=False, verbose_name='Maghrib Time', null=True)
    isha = models.TimeField(auto_now=False, auto_now_add=False, verbose_name='Isha Time', null=True)

    class Meta:
        verbose_name_plural = 'Paryer Timing'
