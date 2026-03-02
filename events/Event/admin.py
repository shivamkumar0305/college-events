from django.contrib import admin
from .models import Category,Event

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug',]
    prepopulated_fields = {'slug': ('name',)}  # Auto-generate slug from name
    search_fields = ['name']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Event)