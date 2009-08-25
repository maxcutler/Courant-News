from django.contrib import admin
from models import Message, DontSendEntry, MessageLog, MessageJob

class MessageJobAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_address', 'subject', 'priority', 'processed', 'created_at', 'processed_at')
    list_filter = ('processed', 'priority')
    ordering = ('-created_at',)
    

class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'to_address', 'subject', 'when_added', 'priority')

class DontSendEntryAdmin(admin.ModelAdmin):
    list_display = ('to_address', 'when_added')

class MessageLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'to_address', 'subject', 'when_attempted', 'result')

admin.site.register(MessageJob, MessageJobAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(DontSendEntry, DontSendEntryAdmin)
admin.site.register(MessageLog, MessageLogAdmin)
