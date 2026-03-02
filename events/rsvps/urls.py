from django.urls import path
from .views import (
    RSVPCreateView,
    MyRSVPsView,
    CancelRSVPView,
    EventAttendeesView,
    DownloadAttendeesView
)

urlpatterns = [
    path('rsvps/', RSVPCreateView.as_view(), name='rsvp-create'),
    path('rsvps/my-rsvps/', MyRSVPsView.as_view(), name='my-rsvps'),
    path('rsvps/<int:pk>/cancel/', CancelRSVPView.as_view(), name='rsvp-cancel'),
    path('events/<int:event_id>/attendees/', EventAttendeesView.as_view(), name='event-attendees'),
    path('events/<int:event_id>/attendees/download/', DownloadAttendeesView.as_view(), name='download-attendees'),
]