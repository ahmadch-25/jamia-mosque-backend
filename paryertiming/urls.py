from django.urls import path, include
from .views import GetPrayerTiming

urlpatterns = [
    path('getprayertiming/', GetPrayerTiming.as_view()),
]
