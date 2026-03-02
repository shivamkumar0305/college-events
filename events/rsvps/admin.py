from django.contrib import admin
from .models import RSVP

class RSVPAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'status', 'rsvp_datetime', 'attended']
    list_filter = ['status', 'attended', 'rsvp_datetime']
    search_fields = ['user__email', 'event__title']
    readonly_fields = ['rsvp_datetime']

admin.site.register(RSVP, RSVPAdmin)
