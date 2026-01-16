from decimal import Decimal
from .models import Product


def get_cart(request):
    """Получить корзину из сессии"""
    cart = request.session.get('cart', {})
    return cart


def add_to_cart(request, product_id, quantity=1):
    """Добавить товар в корзину"""
    cart = get_cart(request)
    product_id = str(product_id)
    
    if product_id in cart:
        cart[product_id]['quantity'] += quantity
    else:
        cart[product_id] = {'quantity': quantity}
    
    request.session['cart'] = cart
    request.session.modified = True
    return cart


def remove_from_cart(request, product_id):
    """Удалить товар из корзины"""
    cart = get_cart(request)
    product_id = str(product_id)
    
    if product_id in cart:
        del cart[product_id]
        request.session['cart'] = cart
        request.session.modified = True
    
    return cart


def update_cart_item(request, product_id, quantity):
    """Обновить количество товара в корзине"""
    cart = get_cart(request)
    product_id = str(product_id)
    
    if product_id in cart:
        if quantity > 0:
            cart[product_id]['quantity'] = quantity
        else:
            del cart[product_id]
        request.session['cart'] = cart
        request.session.modified = True
    
    return cart


def clear_cart(request):
    """Очистить корзину"""
    request.session['cart'] = {}
    request.session.modified = True


def get_cart_items(request):
    """Получить товары корзины с полной информацией"""
    cart = get_cart(request)
    cart_items = []
    total_price = Decimal('0')
    
    for product_id, item_data in cart.items():
        try:
            product = Product.objects.get(id=int(product_id), is_published=True)
            quantity = item_data.get('quantity', 1)
            item_total = product.price * quantity
            total_price += item_total
            
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total': item_total,
            })
        except Product.DoesNotExist:
            continue
    
    return cart_items, total_price


def get_cart_total_quantity(request):
    """Получить общее количество товаров в корзине"""
    cart = get_cart(request)
    return sum(item.get('quantity', 0) for item in cart.values())
