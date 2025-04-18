app_name = 'baby_shop'
from django.urls import path
from .views import ProductListView, ProductDetailView, CategoryListView

urlpatterns = [
    path('', ProductListView.as_view(), name='baby_product_list'),
    path('categories/', CategoryListView.as_view(), name='baby_category_list'),
    path('category/<slug:category_slug>/', ProductListView.as_view(), name='baby_product_list_by_category'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='baby_product_detail'),
]