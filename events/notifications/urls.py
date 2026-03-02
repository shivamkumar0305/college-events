from django.urls import path
from .views import (
    NotificationListView,
    MarkNotificationReadView,
    UnreadNotificationCountView
)

urlpatterns = [
    path('notifications/', NotificationListView.as_view()),
    path('notifications/<int:pk>/read/', MarkNotificationReadView.as_view()),
    path('notifications/unread-count/', UnreadNotificationCountView.as_view()),
]