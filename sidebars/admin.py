from django.contrib import admin
from .models import SideBar, FooterLink


# Register your models here.
@admin.register(SideBar)
class SideBarAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'created_at', 'updated_at')
    list_filter = ('title',)


@admin.register(FooterLink)
class FooterLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'created_at', 'updated_at')
