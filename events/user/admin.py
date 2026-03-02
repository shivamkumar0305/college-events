from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    # What fields to display in the user list
    list_display = ['email', 'username', 'role', 'is_verified_organizer', 'is_staff', 'created_at']
    
    # Add filters in the sidebar
    list_filter = ['role', 'is_verified_organizer', 'is_staff', 'is_active']
    
    # Make these fields searchable
    search_fields = ['email', 'username', 'organization_name', 'college']
    
    # Add your custom fields to the admin form
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role & Verification', {
            'fields': ('role', 'is_verified_organizer')
        }),
        ('Student Info', {
            'fields': ('college', 'branch', 'year')
        }),
        ('Organizer Info', {
            'fields': ('organization_name',)
        }),
        ('Profile', {
            'fields': ('phone', 'profile_picture', 'bio')
        }),
    )

admin.site.register(User, UserAdmin)
