from django.contrib import admin

from .forms import RSSItemForm, SourceForm
from .models import RSSItem, Source


@admin.register(RSSItem)
class RSSItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'pub_date', 'link')
    list_filter = ('pub_date', )
    form = RSSItemForm


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'url', 'status')
    list_filter = ('status', )
    form = SourceForm
