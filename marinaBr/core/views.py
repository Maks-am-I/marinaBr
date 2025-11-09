from django.shortcuts import render
from django.http import HttpResponse

from .models import Product


def index(request):
    products = Product.objects.all()

    context = {
        'products':products
    }

    return render(request, 'core/index.html', context)