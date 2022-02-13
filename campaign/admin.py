from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import DonationItems, CampaignContribution, CampaignType


@admin.register(CampaignType)
class CampaignTypesAdmin(admin.ModelAdmin):
    list_display = ('title', )
    list_filter = ('title', )


@admin.register(DonationItems)
class DonationItemsAdmin(SummernoteModelAdmin):
    list_display = ('title', 'goal_amount', 'end_date', 'currency', 'publish')
    summernote_fields = ('description',)
    list_filter = ('title',)


@admin.register(CampaignContribution)
class CampaignContributionAdmin(admin.ModelAdmin):
    list_display = ('user', 'campaign', 'amount', 'created_on')
    list_filter = ('user', )