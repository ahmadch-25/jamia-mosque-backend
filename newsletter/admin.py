from django.contrib import admin
from .models import NewsLetter


# Register your models here.


@admin.register(NewsLetter)
class NewsLetterAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        print(obj.title)
        super().save_model(request, obj, form, change)
    list_display = ('title', 'description', 'attachment', 'release_date',)
    list_filter = ('title', 'release_date',)



