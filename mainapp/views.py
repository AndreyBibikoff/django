import random

from django.shortcuts import render, get_object_or_404

# Create your views here./
from basketapp.models import Basket
from mainapp.models import ProductCategory, Product


def get_hot_product():
    products = Product.objects.all()

    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)

    return same_products


hot_product = get_hot_product()
same_product = get_same_products(hot_product)


def products(request, pk=None):
    title = 'geekshop - каталог'
    products_menu = ProductCategory.objects.all()

    if pk is not None:
        if pk == 0:
            products = Product.objects.all().order_by('name')
            category = {'category_name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk).order_by('name')

        context = {
            'title': title,
            'products_menu': products_menu,
            'products': products,
            'category': category,
            'basket': get_basket(request.user),
            'hot_product': hot_product,
            'same_product': same_product,
        }

        return render(request, 'mainapp/products.html', context=context)

    context = {
        'title': title,
        'products_menu': products_menu,
        'hot_product': hot_product,
        'same_product': same_product,
        'basket': get_basket(request.user),
    }

    return render(request, 'mainapp/products.html', context=context)


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []


def product(request, pk):
    title = 'продукты'

    content = {
        'title': title,
        'links_menu': ProductCategory.objects.all(),
        'product': get_object_or_404(Product, pk=pk),
        'basket': get_basket(request.user),
    }

    return render(request, 'mainapp/product.html', content)
