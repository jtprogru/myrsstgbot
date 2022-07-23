from django.contrib import admin

from .models import ChannelType, Channel, Message

admin.site.register(ChannelType)
admin.site.register(Channel)
admin.site.register(Message)

