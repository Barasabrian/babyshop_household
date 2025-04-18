from django.contrib import admin
from .models import BabyProduct, BabyProductCategory

@admin.register(BabyProduct)
class BabyProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'is_active']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['-created_at']

@admin.register(BabyProductCategory)
class BabyProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']