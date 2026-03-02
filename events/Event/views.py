from rest_framework import generics, filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Event, Category
from .serializers import EventSerializer, CategorySerializer
from .permissions import IsVerifiedOrganizerOrReadOnly


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class EventListCreateView(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsVerifiedOrganizerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    filterset_fields = ['categories', 'is_online', 'is_featured']
    search_fields = ['title', 'description', 'tags', 'organization_name']
    ordering_fields = ['start_datetime', 'created_at', 'view_count']
    ordering = ['start_datetime']
    
    def get_queryset(self):
        return Event.objects.filter(
            is_registration_open=True
        ).select_related('organizer').prefetch_related('categories')


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsVerifiedOrganizerOrReadOnly]
    lookup_field = 'id'
    
    def get_queryset(self):
        return Event.objects.select_related('organizer').prefetch_related('categories')
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.view_count += 1
        instance.save(update_fields=['view_count'])
        return super().retrieve(request, *args, **kwargs)