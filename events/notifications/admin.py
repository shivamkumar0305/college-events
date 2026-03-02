from django.contrib import admin
from .models import Notification

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification_type', 'title', 'is_read', 'is_emailed', 'created_at']
    list_filter = ['notification_type', 'is_read', 'is_emailed', 'created_at']
    search_fields = ['user__email', 'title', 'message']
    readonly_fields = ['created_at']

admin.site.register(Notification, NotificationAdmin)

