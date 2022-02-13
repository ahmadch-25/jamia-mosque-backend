from django.contrib import admin
from .models import NewsLetter, Subscriber


# Register your models here.


@admin.register(NewsLetter)
class NewsLetterAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'attachment', 'release_date',)
    list_filter = ('title', 'release_date',)


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('user', 'device_token', 'subscription_date',)
    list_filter = ('user',)
