from django.contrib import admin

from .models import StartupModel, NewsDetail

# Register your models here.
admin.site.register(StartupModel)


# News detail admin
class NewsDetailAdmin(admin.ModelAdmin):
    list_display = ('base_url', 'title', 'get_status_display')
    list_filter = ('status', 'base_url')


admin.site.register(NewsDetail, NewsDetailAdmin)
