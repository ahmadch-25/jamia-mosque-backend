from rest_framework import serializers
from .models import SideBar, FooterLink


class SideBarSerializer(serializers.ModelSerializer):
    class Meta:
        model = SideBar
        fields = ['title', 'link', ]


class FooterLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterLink
        fields = ['title', 'link', ]
