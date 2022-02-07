import random

from django.shortcuts import render, get_object_or_404


from mainapp.models import ProductCategory, Product
from django.conf import settings
from django.core.cache import cache


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)

def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True)
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True)


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)

def get_products_orderd_by_price():
    if settings.LOW_CACHE:
        key = 'products_orderd_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).order_by('price')


def get_products_in_category_orderd_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_orderd_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')


def get_hot_product():
    products = get_products()

    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)

    return same_products





def products(request, pk=None):
    title = 'geekshop - каталог'
    products_menu = get_links_menu()
    hot_product = get_hot_product()
    same_product = get_same_products(hot_product)

    if pk is not None:
        if pk == 0:
            products = get_products_orderd_by_price()
            category = {'category_name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = get_products_in_category_orderd_by_price()

        context = {
            'title': title,
            'products_menu': products_menu,
            'products': products,
            'category': category,
            'hot_product': hot_product,
            'same_product': same_product,
        }

        return render(request, 'mainapp/products.html', context=context)

    context = {
        'title': title,
        'products_menu': products_menu,
        'hot_product': hot_product,
        'same_product': same_product,
    }

    return render(request, 'mainapp/products.html', context=context)


def product(request, pk):
    title = 'продукты'

    content = {
        'title': title,
        'links_menu': get_links_menu(),
        'product': get_object_or_404(Product, pk=pk),
    }

    return render(request, 'mainapp/product.html', content)
