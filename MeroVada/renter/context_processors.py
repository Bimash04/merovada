# renter/context_processors.py
from .models import Cart

def cart_item_count(request):
    """Adds the total number of items in the cart to the template context."""
    if request.user.is_authenticated:
        cart_count = Cart.objects.filter(user=request.user).count()
    else:
        cart = request.session.get('cart', {})
        cart_count = sum(cart.values())
    return {'cart_item_count': cart_count}