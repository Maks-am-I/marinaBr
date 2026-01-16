from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from decimal import Decimal
import json

from .models import Product, Category, Order, OrderItem
from .forms import OrderForm
from .cart_utils import (
    add_to_cart, remove_from_cart, update_cart_item,
    get_cart_items, get_cart_total_quantity, clear_cart
)

from django.db.models.functions import Length

def index(request):
    categories = Category.objects.annotate(name_length=Length('title')).order_by('name_length')
    products = Product.objects.filter(is_published='True')

    context = {
        'categories': categories,
        'products' : products,
    }

    return render(request, 'core/index.html', context)


def cart_view(request):
    """Просмотр корзины"""
    cart_items, total_price = get_cart_items(request)
    form = OrderForm()
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'form': form,
    }
    
    return render(request, 'core/cart.html', context)


@require_POST
def add_to_cart_view(request, product_id):
    """Добавить товар в корзину"""
    product = get_object_or_404(Product, id=product_id, is_published=True)
    quantity = int(request.POST.get('quantity', 1))
    
    add_to_cart(request, product_id, quantity)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # AJAX запрос
        cart_total = get_cart_total_quantity(request)
        return JsonResponse({
            'success': True,
            'cart_total': cart_total,
            'message': f'{product.title} добавлен в корзину'
        })
    
    return redirect('cart')


@require_POST
def remove_from_cart_view(request, product_id):
    """Удалить товар из корзины"""
    remove_from_cart(request, product_id)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart_total = get_cart_total_quantity(request)
        cart_items, total_price = get_cart_items(request)
        return JsonResponse({
            'success': True,
            'cart_total': cart_total,
            'total_price': str(total_price)
        })
    
    return redirect('cart')


@require_POST
def update_cart_item_view(request, product_id):
    """Обновить количество товара в корзине"""
    quantity = int(request.POST.get('quantity', 1))
    update_cart_item(request, product_id, quantity)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart_total = get_cart_total_quantity(request)
        cart_items, total_price = get_cart_items(request)
        
        # Найти обновленный товар
        item_total = Decimal('0')
        for item in cart_items:
            if item['product'].id == int(product_id):
                item_total = item['total']
                break
        
        return JsonResponse({
            'success': True,
            'cart_total': cart_total,
            'item_total': str(item_total),
            'total_price': str(total_price)
        })
    
    return redirect('cart')


def get_cart_info(request):
    """Получить информацию о корзине для AJAX"""
    cart_total = get_cart_total_quantity(request)
    cart_items, total_price = get_cart_items(request)
    
    return JsonResponse({
        'cart_total': cart_total,
        'total_price': str(total_price)
    })


def create_order(request):
    """Создать заказ"""
    if request.method == 'POST':
        cart_items, total_price = get_cart_items(request)
        
        if not cart_items:
            messages.error(request, 'Ваша корзина пуста')
            return redirect('cart')
        
        form = OrderForm(request.POST)
        
        if form.is_valid():
            # Создать заказ
            order = Order.objects.create(
                customer_name=form.cleaned_data['customer_name'],
                customer_phone=form.cleaned_data['customer_phone'],
                order_date=form.cleaned_data['order_date'],
                order_time=form.cleaned_data['order_time'],
                delivery_address=form.cleaned_data['delivery_address'],
                total_price=total_price,
                status='new'
            )
            
            # Создать товары заказа
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['product'].price
                )
            
            # Очистить корзину
            clear_cart(request)
            
            messages.success(request, f'Заказ #{order.id} успешно оформлен! Мы свяжемся с вами в ближайшее время.')
            return redirect('index')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме')
    else:
        form = OrderForm()
    
    # Если GET запрос или форма невалидна, показать корзину с формой
    cart_items, total_price = get_cart_items(request)
    
    if not cart_items:
        return redirect('cart')
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'form': form,
    }
    
    return render(request, 'core/cart.html', context)