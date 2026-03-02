from django.db.models.signals import post_save
from django.dispatch import receiver
from rsvps.models import RSVP
from Event.models import Event
from .models import Notification


@receiver(post_save, sender=RSVP)
def create_rsvp_notification(sender, instance, created, **kwargs):
    if created and instance.status == 'confirmed':
        Notification.objects.create(
            user=instance.user,
            event=instance.event,
            notification_type='rsvp_confirmed',
            title="RSVP Confirmed",
            message=f"You have successfully RSVPed to {instance.event.title}"
        )
@receiver(post_save, sender=Event)
def notify_event_update(sender, instance, created, **kwargs):
    if not created:
        # Get all confirmed attendees
        rsvps = instance.rsvps.filter(status='confirmed')

        for rsvp in rsvps:
            Notification.objects.create(
                user=rsvp.user,
                event=instance,
                notification_type='event_update',
                title="Event Updated",
                message=f"The event '{instance.title}' has been updated. Check details."
            )