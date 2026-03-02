from django.db import models
from django.conf import settings

class RSVP(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('waitlist', 'Waitlist'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='rsvps'
    )
    event = models.ForeignKey(
        'Event.Event',  # Assuming your app is named 'Event'
        on_delete=models.CASCADE,
        related_name='rsvps'
    )
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    
    # Tracking
    attended = models.BooleanField(default=False)
    rsvp_datetime = models.DateTimeField(auto_now_add=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    
    # Optional notes
    notes = models.TextField(blank=True, help_text="Any special requirements")
    
    class Meta:
        unique_together = ['user', 'event']
        ordering = ['-rsvp_datetime']
        verbose_name = 'RSVP'
        verbose_name_plural = 'RSVPs'
    
    def __str__(self):
        return f"{self.user.email} - {self.event.title}"