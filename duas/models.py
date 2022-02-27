from django.db import models


# Create your models here.
class DuaCategory(models.Model):
    category = models.CharField(max_length=300, verbose_name='Category')


    def __str__(self):
        return self.category

    class Meta:
        verbose_name_plural = 'DuaCategory'

class Duas(models.Model):
    category = models.ForeignKey(DuaCategory,on_delete=models.CASCADE, verbose_name='Category', related_name='duas')
    zekr = models.CharField(max_length=2000, verbose_name='Zekar', null=True, blank=True)
    reference = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.zekr

    class Meta:
        verbose_name_plural = 'Duas'