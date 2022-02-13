from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserInfo
from campaign.models import CampaignContribution, DonationItems
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('phone_number',)


class UserSerializer(serializers.ModelSerializer):
    userinfo = UserInfoSerializer()

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'userinfo',)


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationItems
        fields = ['id', 'campaign_type', 'title', 'currency', ]


class ContributionSerializer(serializers.ModelSerializer):
    campaign = CampaignSerializer()

    class Meta:
        model = CampaignContribution
        fields = ('amount', 'created_on', 'campaign')
