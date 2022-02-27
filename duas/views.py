import json

from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from django.db import connection
from .models import Duas, DuaCategory
# Create your views here.
from rest_framework.views import APIView
from django.http import JsonResponse
from .serializers import DuaCategorySerializer

class GetAllDuas(APIView):

    def get(self, request):
        duas=DuaCategory.objects.all()
        data=DuaCategorySerializer(duas,many=True)

        return JsonResponse(data.data,safe=False)
