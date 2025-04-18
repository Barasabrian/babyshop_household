from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import HouseholdProduct, HouseholdCategory

class HouseholdProductListView(ListView):
    model = HouseholdProduct
    template_name = 'household/list.html'
    context_object_name = 'products'
    paginate_by = 8
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(is_active=True)
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = get_object_or_404(HouseholdCategory, slug=category_slug)
            queryset = queryset.filter(category=category)
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = HouseholdCategory.objects.filter(is_active=True)
        return context

class HouseholdProductDetailView(DetailView):
    model = HouseholdProduct
    template_name = 'household/detail.html'
    context_object_name = 'product'
    
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_products'] = HouseholdProduct.objects.filter(
            category=self.object.category,
            is_active=True
        ).exclude(id=self.object.id)[:4]
        return context

class HouseholdCategoryListView(ListView):
    model = HouseholdCategory
    template_name = 'household/categories.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)