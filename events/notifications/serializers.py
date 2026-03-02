from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    event_title = serializers.CharField(source='event.title', read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id',
            'notification_type',
            'title',
            'message',
            'event',
            'event_title',
            'is_read',
            'created_at'
        ]
        read_only_fields = fields