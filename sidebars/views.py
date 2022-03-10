from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import SideBar, FooterLink
from .serailizers import SideBarSerializer, FooterLinkSerializer


# Create your views here.
class SidebarListView(APIView):
    def get(self, request):
        sidebars = SideBar.objects.all()
        footer_link = FooterLink.objects.all().first()
        side_bars = SideBarSerializer(sidebars, many=True)
        footer_link = FooterLinkSerializer(footer_link)
        response = {"sidebar_list": side_bars.data, "footer_link": footer_link.data}
        return Response(response,
                        status=status.HTTP_200_OK)
