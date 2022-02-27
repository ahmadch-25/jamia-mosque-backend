from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import NewsLetter
from .serialzers import NewsLetterSerializer


class NewsletterView(APIView):

    def get(self, request):
        news_letters = NewsLetter.objects.all()
        news_letters = NewsLetterSerializer(news_letters, many=True)
        return Response(news_letters.data,
                        status=status.HTTP_200_OK)
