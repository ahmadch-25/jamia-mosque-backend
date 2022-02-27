from django.contrib import admin
from .models import DuaCategory, Duas
from import_export import resources
from import_export.admin import ImportExportModelAdmin
# Register your models here.\


class DuasResource(resources.ModelResource):
   class Meta:
      model = DuaCategory


@admin.register(DuaCategory)
class DuaCategoryAdmin(ImportExportModelAdmin):
    resource_class = DuasResource
    list_display = ('id', 'category',)


@admin.register(Duas)
class DuasDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'zekr', 'reference')
