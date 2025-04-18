from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from baby_shop.models import BabyProduct
from household.models import HouseholdProduct
from .models import Cart, CartItem
from django.contrib.auth.decorators import login_required

def get_cart(request):
    cart_id = request.session.get('cart_id')
    if cart_id:
        try:
            cart = Cart.objects.get(id=cart_id)
        except Cart.DoesNotExist:
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.id
    else:
        cart = Cart.objects.create()
        request.session['cart_id'] = cart.id
    return cart

@require_POST
def cart_add(request, product_type, product_id):
    cart = get_cart(request)
    if product_type == 'baby':
        product = get_object_or_404(BabyProduct, id=product_id)
    else:
        product = get_object_or_404(HouseholdProduct, id=product_id)
    
    item, created = CartItem.objects.get_or_create(
        cart=cart,
        **{f"{product_type}_product": product},
        defaults={'quantity': 1}
    )
    if not created:
        item.quantity += 1
        item.save()
    return redirect('cart:cart_detail')

def cart_remove(request, item_id):
    cart = get_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = get_cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})

@login_required
def checkout(request):
    cart = get_cart(request)
    if not cart.items.count():
        return redirect('cart:cart_detail')
    
    if request.method == 'POST':
        # Process order here
        del request.session['cart_id']
        return render(request, 'cart/checkout_done.html')
    
    return render(request, 'cart/checkout.html', {'cart': cart})