from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import DonationItems, CampaignContribution, CampaignType, ZakatNisab


@admin.register(CampaignType)
class CampaignTypesAdmin(admin.ModelAdmin):
    list_display = ('title', )
    list_filter = ('title', )


@admin.register(DonationItems)
class DonationItemsAdmin(admin.ModelAdmin):
    list_display = ('title', 'goal_amount', 'end_date', 'description', 'currency', 'publish',)
    list_filter = ('title',)



@admin.register(CampaignContribution)
class CampaignContributionAdmin(admin.ModelAdmin):
    list_display = ('user', 'campaign', 'amount', 'created_on')
    list_filter = ('user', )

@admin.register(ZakatNisab)
class ZakatNisabAdmin(admin.ModelAdmin):
    list_display = ('nisab_in_usd', 'nisab_in_kes', 'created_on', 'updated_on')