from rest_framework import serializers
from .models import Event, Category
from django.contrib.auth import get_user_model

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon']


class OrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'organization_name', 'profile_picture']


class EventSerializer(serializers.ModelSerializer):
    # Show full category details instead of just ID
    categories = CategorySerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        queryset=Category.objects.all(),
        source='categories'
    )
    
    # Show organizer details
    organizer = OrganizerSerializer(read_only=True)
    
    # Extra computed field
    rsvp_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'slug', 'description',
            'organizer', 'organization_name',
            'categories', 'category_ids',
            'tags',
            'start_datetime', 'end_datetime',
            'venue', 'is_online', 'meeting_link',
            'media_files',
            'max_capacity', 'is_registration_open',
            'is_featured', 'view_count',
            'rsvp_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'slug', 'organizer',
            'view_count', 'created_at', 'updated_at'
        ]
    
    def get_rsvp_count(self, obj):
        return obj.rsvps.filter(status='confirmed').count()
    
    def validate(self, data):
        # End time must be after start time
        if data.get('end_datetime') and data.get('start_datetime'):
            if data['end_datetime'] <= data['start_datetime']:
                raise serializers.ValidationError("End time must be after start time")
        
        # If online event, meeting link is required
        if data.get('is_online') and not data.get('meeting_link'):
            raise serializers.ValidationError("Meeting link is required for online events")
        
        # If not online, venue is required
        if not data.get('is_online') and not data.get('venue'):
            raise serializers.ValidationError("Venue is required for in-person events")
        
        return data
    
    def create(self, validated_data):
        # Automatically set organizer to current user
        validated_data['organizer'] = self.context['request'].user
        return super().create(validated_data)