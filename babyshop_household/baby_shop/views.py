from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q, Avg, Count
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import BabyProduct, BabyProductCategory, ProductReview, ProductImage
from .forms import ProductReviewForm, ProductFilterForm

class ProductListView(ListView):
    model = BabyProduct
    template_name = 'baby_shop/list.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(is_active=True)
        
        # Filter by category if specified
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = get_object_or_404(BabyProductCategory, slug=category_slug)
            queryset = queryset.filter(category=category)
        
        # Apply filters from GET parameters
        self.filters = ProductFilterForm(self.request.GET or None)
        if self.filters.is_valid():
            data = self.filters.cleaned_data
            
            if data.get('age_range'):
                queryset = queryset.filter(age_range=data['age_range'])
            
            if data.get('min_price'):
                queryset = queryset.filter(price__gte=data['min_price'])
            
            if data.get('max_price'):
                queryset = queryset.filter(price__lte=data['max_price'])
            
            if data.get('safety_rating'):
                queryset = queryset.filter(safety_rating__gte=data['safety_rating'])
            
            if data.get('search'):
                queryset = queryset.filter(
                    Q(name__icontains=data['search']) |
                    Q(description__icontains=data['search'])
                )
        
        # Apply sorting
        sort_by = self.request.GET.get('sort_by', '-created_at')
        if sort_by == 'price_asc':
            return queryset.order_by('price')
        elif sort_by == 'price_desc':
            return queryset.order_by('-price')
        elif sort_by == 'rating':
            return queryset.annotate(
                avg_rating=Avg('reviews__rating')
            ).order_by('-avg_rating')
        elif sort_by == 'popularity':
            return queryset.annotate(
                order_count=Count('cart_items')
            ).order_by('-order_count')
        
        return queryset.order_by(sort_by)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = BabyProductCategory.objects.filter(is_active=True)
        context['filter_form'] = self.filters
        context['current_category'] = self.kwargs.get('category_slug')
        return context

class ProductDetailView(DetailView):
    model = BabyProduct
    template_name = 'baby_shop/detail.html'
    context_object_name = 'product'
    
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        
        # Related products (same category)
        context['related_products'] = BabyProduct.objects.filter(
            category=product.category,
            is_active=True
        ).exclude(id=product.id)[:4]
        
        # Review form and reviews
        context['review_form'] = ProductReviewForm()
        context['reviews'] = product.reviews.filter(is_approved=True).order_by('-created_at')
        
        # Average rating
        context['average_rating'] = product.reviews.filter(
            is_approved=True
        ).aggregate(Avg('rating'))['rating__avg']
        
        # Check if user has already reviewed
        if self.request.user.is_authenticated:
            context['user_has_reviewed'] = product.reviews.filter(
                user=self.request.user
            ).exists()
        
        return context

class CategoryListView(ListView):
    model = BabyProductCategory
    template_name = 'baby_shop/categories.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

class AddReviewView(LoginRequiredMixin, CreateView):
    model = ProductReview
    form_class = ProductReviewForm
    
    def form_valid(self, form):
        product = get_object_or_404(BabyProduct, slug=self.kwargs['slug'])
        form.instance.product = product
        form.instance.user = self.request.user
        
        # Check if user has already reviewed this product
        if ProductReview.objects.filter(product=product, user=self.request.user).exists():
            messages.error(self.request, "You've already reviewed this product!")
            return redirect(product.get_absolute_url())
        
        messages.success(self.request, "Thank you for your review!")
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('baby_shop:product_detail', kwargs={'slug': self.kwargs['slug']})

class ProductSearchView(ListView):
    model = BabyProduct
    template_name = 'baby_shop/search_results.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_active=True)
        query = self.request.GET.get('q', '')
        
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # AJAX request - return JSON
            data = [{
                'name': product.name,
                'url': product.get_absolute_url(),
                'image': product.primary_image.url if product.primary_image else '',
                'price': str(product.price)
            } for product in context['products']]
            return JsonResponse(data, safe=False)
        # Regular request - return HTML
        return super().render_to_response(context, **response_kwargs)