from django.db import models
from django.conf import settings

class Notification(models.Model):
    TYPE_CHOICES = [
        ('new_event', 'New Event'),
        ('event_reminder', 'Event Reminder'),
        ('event_update', 'Event Update'),
        ('event_cancelled', 'Event Cancelled'),
        ('rsvp_confirmed', 'RSVP Confirmed'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    event = models.ForeignKey(
        'Event.Event',  # Update this to match your Event app name
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    
    notification_type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    
    is_read = models.BooleanField(default=False)
    is_emailed = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.notification_type}"