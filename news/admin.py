from django.contrib import admin
from .models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """The news admin site."""
    list_display = ['pk', 'title', 'type', 'created_at']
