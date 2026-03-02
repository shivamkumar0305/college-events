from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from .models import RSVP
from Event.models import Event
from .serializers import RSVPSerializer, RSVPListSerializer
from .permissions import IsEventOrganizer
import csv


class RSVPCreateView(generics.CreateAPIView):
    """Student creates RSVP"""
    serializer_class = RSVPSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rsvp = serializer.save()
        
        # Return success message based on status
        if rsvp.status == 'waitlist':
            message = "Event is full. You have been added to the waitlist."
        else:
            message = "RSVP confirmed successfully!"
        
        return Response({
            'message': message,
            'rsvp': RSVPSerializer(rsvp).data
        }, status=status.HTTP_201_CREATED)


class MyRSVPsView(generics.ListAPIView):
    """Current user's all RSVPs"""
    serializer_class = RSVPSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return RSVP.objects.filter(
            user=self.request.user
        ).select_related('event', 'user').order_by('-rsvp_datetime')


class CancelRSVPView(generics.DestroyAPIView):
    """Cancel an RSVP"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return RSVP.objects.filter(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Update status instead of deleting
        from django.utils import timezone
        instance.status = 'cancelled'
        instance.cancelled_at = timezone.now()
        instance.save()
        
        # TODO: Later with Celery - move waitlist person to confirmed
        
        return Response({
            'message': 'RSVP cancelled successfully'
        }, status=status.HTTP_200_OK)


class EventAttendeesView(generics.ListAPIView):
    """Organizer views attendee list for their event"""
    serializer_class = RSVPListSerializer
    permission_classes = [IsAuthenticated, IsEventOrganizer]
    
    def get_queryset(self):
        event_id = self.kwargs.get('event_id')
        event = Event.objects.get(id=event_id)
        
        # Check permission
        self.check_object_permissions(self.request, event)
        
        return RSVP.objects.filter(
            event_id=event_id,
            status='confirmed'
        ).select_related('user').order_by('-rsvp_datetime')


class DownloadAttendeesView(APIView):
    """Download attendee list as CSV"""
    permission_classes = [IsAuthenticated, IsEventOrganizer]
    
    def get(self, request, event_id):
        event = Event.objects.get(id=event_id)
        
        # Check permission
        self.check_object_permissions(request, event)
        
        # Create CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="attendees_{event.slug}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Email', 'Name', 'College', 'Branch', 'Year', 'RSVP Date', 'Notes'])
        
        rsvps = RSVP.objects.filter(
            event=event,
            status='confirmed'
        ).select_related('user')
        
        for rsvp in rsvps:
            writer.writerow([
                rsvp.user.email,
                rsvp.user.username,
                rsvp.user.college,
                rsvp.user.branch,
                rsvp.user.year,
                rsvp.rsvp_datetime.strftime('%Y-%m-%d %H:%M'),
                rsvp.notes
            ])
        
        return response