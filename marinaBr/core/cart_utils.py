from decimal import Decimal
from .models import Product, ReadySolution


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


def add_ready_solution_to_cart(request, solution_id, quantity=1):
    """Добавить готовое решение в корзину"""
    cart = get_cart(request)
    item_key = f'ready_solution_{solution_id}'
    
    if item_key in cart:
        cart[item_key]['quantity'] += quantity
    else:
        cart[item_key] = {'quantity': quantity, 'type': 'ready_solution'}
    
    request.session['cart'] = cart
    request.session.modified = True
    return cart


def remove_ready_solution_from_cart(request, solution_id):
    """Удалить готовое решение из корзины"""
    cart = get_cart(request)
    item_key = f'ready_solution_{solution_id}'
    
    if item_key in cart:
        del cart[item_key]
        request.session['cart'] = cart
        request.session.modified = True
    
    return cart


def update_ready_solution_cart_item(request, solution_id, quantity):
    """Обновить количество готового решения в корзине"""
    cart = get_cart(request)
    item_key = f'ready_solution_{solution_id}'
    
    if item_key in cart:
        if quantity > 0:
            cart[item_key]['quantity'] = quantity
        else:
            del cart[item_key]
        request.session['cart'] = cart
        request.session.modified = True
    
    return cart


def get_cart_items(request):
    """Получить товары корзины с полной информацией (продукты и готовые решения)"""
    cart = get_cart(request)
    cart_items = []
    total_price = Decimal('0')
    
    for item_key, item_data in cart.items():
        quantity = item_data.get('quantity', 1)
        
        if item_key.startswith('ready_solution_'):
            # Готовое решение
            try:
                solution_id = int(item_key.replace('ready_solution_', ''))
                solution = ReadySolution.objects.get(id=solution_id, is_published=True)
                item_total = solution.price * quantity
                total_price += item_total
                
                cart_items.append({
                    'ready_solution': solution,
                    'quantity': quantity,
                    'total': item_total,
                    'type': 'ready_solution',
                })
            except ReadySolution.DoesNotExist:
                continue
        else:
            # Обычный продукт
            try:
                product_id = int(item_key)
                product = Product.objects.get(id=product_id, is_published=True)
                item_total = product.price * quantity
                total_price += item_total
                
                cart_items.append({
                    'product': product,
                    'quantity': quantity,
                    'total': item_total,
                    'type': 'product',
                })
            except (Product.DoesNotExist, ValueError):
                continue
    
    return cart_items, total_price


def get_cart_total_quantity(request):
    """Получить общее количество товаров в корзине"""
    cart = get_cart(request)
    return sum(item.get('quantity', 0) for item in cart.values())
