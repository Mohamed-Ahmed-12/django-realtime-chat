from django.contrib import admin
from . import models

admin.site.site_header = "Chat App"
admin.site.site_url = "/chat/0/"

# Register your models here.
class ChatRoomAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj and obj.pk is not None:
            # Make the fields read-only after the object has been created
            return self.readonly_fields + ('member',)
        return self.readonly_fields

admin.site.register(models.ChatRoom, ChatRoomAdmin)

class ChatMessageAdmin(admin.ModelAdmin):
    search_fields = ('read',)

admin.site.register(models.ChatMessage , ChatMessageAdmin)
admin.site.register(models.AudioVideo)

admin.site.register(models.VideoCall)

