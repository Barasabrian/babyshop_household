from .models import Cart

def cart(request):
    cart_id = request.session.get('cart_id')
    if cart_id:
        try:
            cart = Cart.objects.get(id=cart_id)
            return {'cart': cart}
        except Cart.DoesNotExist:
            del request.session['cart_id']
    return {'cart': None}