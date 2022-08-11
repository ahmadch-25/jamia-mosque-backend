from django.db import models
from django.contrib.auth.models import User


class CampaignType(models.Model):
    title = models.CharField(max_length=50, verbose_name='Campaign Type')

    def __str__(self):
        return self.title


class DonationItems(models.Model):
    DEFAULT_CURRENCY = 'KES'
    CURRENCY_TYPE_CHOICES = (
        ('USD', 'USD'),
        ('KES', 'KES'),
    )
    campaign_type = models.ForeignKey(CampaignType, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100, verbose_name='Title')
    image = models.ImageField(verbose_name='Image',upload_to='uploads/', null=True, blank=True)
    description = models.TextField()
    goal_amount = models.IntegerField(verbose_name='Goal Amount')
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    end_date = models.DateTimeField(verbose_name='End Date')
    currency = models.CharField(max_length=3, choices=CURRENCY_TYPE_CHOICES, verbose_name='Currency',
                                default=DEFAULT_CURRENCY)
    contribution_amount = models.IntegerField(verbose_name='Contribution Amount', null=True, blank=True, default=0)
    publish = models.BooleanField()

    def __str__(self):
        return self.campaign_type.title + "   -   " + self.title

    class Meta:
        verbose_name_plural = 'Donation Items'
        ordering = ['-created_on']


class CampaignContribution(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    campaign = models.ForeignKey(DonationItems, on_delete=models.CASCADE, null=True,
                                 related_name='campaign_contributions')
    amount = models.IntegerField(verbose_name='Amount')
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.user.username + "     -    " + str(self.amount)

    class Meta:
        verbose_name_plural = 'Contributions'
        ordering = ['-amount']


class ZakatNisab(models.Model):
    nisab_in_usd = models.FloatField(verbose_name='Nisab in USD')
    nisab_in_kes = models.FloatField(verbose_name='Nisab in KES')
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return str(self.nisab_in_usd) + "     -    " + str(self.nisab_in_kes)

    class Meta:
        verbose_name_plural = 'Zakat Nisab'
        ordering = ['-updated_on']
