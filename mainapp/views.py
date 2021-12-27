from django.shortcuts import render, get_object_or_404

# Create your views here./
from basketapp.models import Basket
from mainapp.models import ProductCategory, Product


def products(request, pk=None):
    title = 'geekshop - каталог'
    products_menu = ProductCategory.objects.all()
    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

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
            'basket': basket,
        }

        return render(request, 'mainapp/products.html', context=context)

    same_product = Product.objects.all()

    context = {
        'title': title,
        'products_menu': products_menu,
        'products': same_product,
    }

    return render(request, 'mainapp/products.html', context=context)
