app_name ='household'
from django.urls import path
from .views import HouseholdProductListView, HouseholdProductDetailView, HouseholdCategoryListView

urlpatterns = [
    path('', HouseholdProductListView.as_view(), name='product_list'),
    path('categories/', HouseholdCategoryListView.as_view(), name='category_list'),
    path('category/<slug:category_slug>/', HouseholdProductListView.as_view(), name='product_list_by_category'),
    path('<slug:slug>/', HouseholdProductDetailView.as_view(), name='product_detail'),
]