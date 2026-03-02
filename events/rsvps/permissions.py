from rest_framework.permissions import BasePermission

class IsEventOrganizer(BasePermission):
    """
    Only the event's organizer can see attendee list
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # obj is the Event
        return obj.organizer == request.user