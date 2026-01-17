from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from decimal import Decimal
import json

from .models import Product, Category, Order, OrderItem
from .forms import OrderForm, ContactForm
from .cart_utils import (
    add_to_cart, remove_from_cart, update_cart_item,
    get_cart_items, get_cart_total_quantity, clear_cart
)

from django.db.models.functions import Length

def index(request):
    categories = Category.objects.annotate(name_length=Length('title')).order_by('name_length')
    products = Product.objects.filter(is_published=True, is_bundle=False).select_related('category').prefetch_related('bundle_items')
    bundle_products = Product.objects.filter(is_published=True, is_bundle=True).select_related('category').prefetch_related('bundle_items__product').order_by('persons_count')
    
    form = ContactForm()
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Отправить email
            try:
                admin_email = getattr(settings, 'ADMIN_EMAIL', settings.DEFAULT_FROM_EMAIL)
                if admin_email:
                    subject = 'Новая заявка с сайта Maria Br'
                    question_text = form.cleaned_data.get('question', '').strip() or 'Не указан'
                    message = f"""
Новая заявка с формы обратной связи:

Имя: {form.cleaned_data['name']}
Телефон: {form.cleaned_data['phone']}
Вопрос: {question_text}
"""
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL or settings.EMAIL_HOST_USER,
                        [admin_email],
                        fail_silently=False,
                    )
                    messages.success(request, 'Спасибо! Ваша заявка отправлена. Мы свяжемся с вами в ближайшее время.')
                    form = ContactForm()  # Очистить форму после отправки
                else:
                    messages.error(request, 'Извините, произошла ошибка. Попробуйте позже.')
            except Exception as e:
                messages.error(request, 'Извините, произошла ошибка при отправке заявки. Попробуйте позже.')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')

    context = {
        'categories': categories,
        'products': products,
        'bundle_products': bundle_products,
        'form': form,
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
            order_items_text = []
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['product'].price
                )
                order_items_text.append(f"- {item['product'].title} x{item['quantity']} = {item['total']} ₽")
            
            # Отправить email с заказом
            try:
                admin_email = getattr(settings, 'ADMIN_EMAIL', settings.DEFAULT_FROM_EMAIL)
                if admin_email:
                    subject = f'Новый заказ #{order.id} с сайта Maria Br'
                    message = f"""
Новый заказ с сайта:

Номер заказа: #{order.id}
Имя клиента: {order.customer_name}
Телефон: {order.customer_phone}
Дата заказа: {order.order_date}
Время заказа: {order.order_time}
Адрес доставки: {order.delivery_address}

Товары:
{chr(10).join(order_items_text)}

Общая сумма: {order.total_price} ₽

Статус: {order.get_status_display()}
"""
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL or settings.EMAIL_HOST_USER,
                        [admin_email],
                        fail_silently=False,
                    )
            except Exception as e:
                # Логируем ошибку, но не прерываем создание заказа
                pass
            
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