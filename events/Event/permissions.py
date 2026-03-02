from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsVerifiedOrganizerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Anyone can read (GET requests)
        if request.method in SAFE_METHODS:
            return True
        
        # For write operations (POST/PUT/DELETE)
        # Must be logged in + verified organizer
        return (
            request.user.is_authenticated and
            request.user.role == 'organizer' and
            request.user.is_verified_organizer
        )
    
    def has_object_permission(self, request, view, obj):
        # Anyone can read
        if request.method in SAFE_METHODS:
            return True
        
        # Only the organizer who created the event can edit/delete
        return obj.organizer == request.user