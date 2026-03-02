from rest_framework import serializers
from .models import RSVP
from Event.serializers import EventSerializer
from user.serializers import UserSerializer
from Event.models import Event


class RSVPSerializer(serializers.ModelSerializer):
    # Show full event details when reading
    event_details = EventSerializer(source='event', read_only=True)
    user_details = UserSerializer(source='user', read_only=True)
    
    # For creating RSVP, just send event ID
    event = serializers.PrimaryKeyRelatedField(
        queryset=Event.objects.all(),
        write_only=True
    )
    
    class Meta:
        model = RSVP
        fields = [
            'id', 'user', 'user_details',
            'event', 'event_details',
            'status', 'attended',
            'rsvp_datetime', 'cancelled_at',
            'notes'
        ]
        read_only_fields = ['id', 'user', 'status', 'rsvp_datetime', 'cancelled_at', 'attended']
    
    def validate(self, data):
        request = self.context.get('request')
        event = data.get('event')
        
        # Check if user already RSVPed
        if RSVP.objects.filter(user=request.user, event=event).exists():
            raise serializers.ValidationError("You have already RSVPed to this event")
        
        # Check if registration is open
        if not event.is_registration_open:
            raise serializers.ValidationError("Registration is closed for this event")
        
        # Check if user is the organizer
        if event.organizer == request.user:
            raise serializers.ValidationError("Organizers cannot RSVP to their own events")
        
        return data
    
    def create(self, validated_data):
        request = self.context.get('request')
        event = validated_data['event']
        
        # Check if event is full
        current_rsvps = event.rsvps.filter(status='confirmed').count()
        
        if event.max_capacity and current_rsvps >= event.max_capacity:
            # Add to waitlist
            validated_data['status'] = 'waitlist'
        else:
            validated_data['status'] = 'confirmed'
        
        validated_data['user'] = request.user
        return super().create(validated_data)


class RSVPListSerializer(serializers.ModelSerializer):
    """Simpler serializer for organizer's attendee list"""
    user_email = serializers.CharField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    user_college = serializers.CharField(source='user.college', read_only=True)
    user_branch = serializers.CharField(source='user.branch', read_only=True)
    user_year = serializers.IntegerField(source='user.year', read_only=True)
    
    class Meta:
        model = RSVP
        fields = [
            'id', 'user_email', 'user_name',
            'user_college', 'user_branch', 'user_year',
            'status', 'attended', 'rsvp_datetime', 'notes'
        ]