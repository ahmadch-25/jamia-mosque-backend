from rest_framework import serializers
from .models import DonationItems


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationItems
        fields = ['id','campaign_type', 'title', 'description', 'image', 'goal_amount', 'end_date', 'currency']