from django.urls import path
from .views import EventListCreateView, EventDetailView, CategoryListView

urlpatterns = [
    path('events/', EventListCreateView.as_view(), name='event-list-create'),
    path('events/<int:id>/', EventDetailView.as_view(), name='event-detail'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
]