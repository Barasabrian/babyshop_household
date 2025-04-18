app_name = 'cart'
from django.urls import path
from .views import cart_detail, cart_add, cart_remove, checkout

urlpatterns = [
    path('', cart_detail, name='cart_detail'),
    path('add/baby/<int:product_id>/', cart_add, name='cart_add_baby'),
    path('add/household/<int:product_id>/', cart_add, name='cart_add_household'),
    path('remove/<int:item_id>/', cart_remove, name='cart_remove'),
    path('checkout/', checkout, name='checkout'),
]