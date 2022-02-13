from django.db import models
from django.contrib.auth.models import User


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, )
    phone_number = models.CharField(max_length=50, verbose_name='Phone Number', null=True, blank=True)
    device_token = models.CharField(max_length=500, verbose_name='device token')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'User'
