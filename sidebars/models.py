from django.db import models


# Create your models here.
class SideBar(models.Model):
    title = models.CharField(max_length=50, verbose_name='Sidebar Title')
    link = models.CharField(max_length=200, verbose_name='Sidebar link')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Sidebars'


class FooterLink(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title')
    link = models.CharField(max_length=200, verbose_name='Link')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'footerLink'
