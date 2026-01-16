from .cart_utils import get_cart_total_quantity, get_cart_items


def cart(request):
    """Context processor для корзины"""
    cart_total = get_cart_total_quantity(request)
    cart_items, total_price = get_cart_items(request)
    
    return {
        'cart_total': cart_total,
        'cart_total_price': total_price,
    }
