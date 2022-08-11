from django.http import JsonResponse
from rest_framework.views import APIView
from .models import PrayerTiming
from .serializers import PrayerTimingSerializer


class GetPrayerTiming(APIView):
    def get(self, request):
        prayers = PrayerTiming.objects.first()
        data = PrayerTimingSerializer(prayers)
        return JsonResponse(data.data, safe=False)
