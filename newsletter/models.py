from django.db import models
from django.contrib.auth.models import User


class NewsLetter(models.Model):
    title = models.CharField(max_length=50, verbose_name='Title')
    description = models.TextField(max_length=280, verbose_name='Summary Message')
    attachment = models.FileField(verbose_name='Attachment', upload_to='newsletter_uploads')
    release_date = models.DateTimeField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Mosque News Letters'
        ordering = ['-release_date']


class Subscriber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, )
    device_token = models.CharField(max_length=255, verbose_name='Device Token')
    subscription_date = models.DateTimeField(auto_now_add=True, verbose_name='Subscription Date')

    def __str__(self):
        return self.user.username
