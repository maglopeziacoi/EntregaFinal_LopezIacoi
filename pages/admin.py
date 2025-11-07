from django.contrib import admin
from .models import Page


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'published_at')
    list_filter = ('status', 'published_at')
    search_fields = ('title', 'summary', 'content')
    prepopulated_fields = { 'slug': ('title',) }