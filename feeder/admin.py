from django.contrib import admin

from .forms import RSSItemForm, TaskForm
from .models import RSSItem, Task


@admin.register(RSSItem)
class RSSItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'pub_date', 'link')
    list_filter = ('pub_date', )
    form = RSSItemForm


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'url', 'status')
    list_filter = ('status', )
    form = TaskForm
