from django.contrib import admin
from .models import HouseholdProduct, HouseholdCategory

@admin.register(HouseholdProduct)
class HouseholdProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'is_active']
    list_filter = ['category', 'material', 'is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['-created_at']

@admin.register(HouseholdCategory)
class HouseholdCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'room_type', 'slug', 'is_active']
    list_filter = ['room_type', 'is_active']
    prepopulated_fields = {'slug': ('name',)}