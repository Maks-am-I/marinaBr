from django.shortcuts import render


from .models import Product, Category

from django.db.models.functions import Length

def index(request):
    categories = Category.objects.annotate(name_length=Length('title')).order_by('name_length')
    products = Product.objects.filter(is_published='True')

    context = {
        'categories': categories,
        'products' : products,
    }

    return render(request, 'core/index.html', context)