app_name = 'baby_shop'
from django.urls import path
from .views import ProductListView, ProductDetailView, CategoryListView, ProductSearchView

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('category/<slug:category_slug>/', ProductListView.as_view(), name='product_list_by_category'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('search/', ProductSearchView.as_view(), name='product_search'),  
]