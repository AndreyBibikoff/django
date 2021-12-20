from django.shortcuts import render


# Create your views here./
from mainapp.models import ProductCategory


def products(request):
    title = 'geekshop - каталог'
    products_menu = ProductCategory.objects.all()

    context = {
        'title': title,
        'products_menu': products_menu,

    }
    return render(request, 'mainapp/products.html', context=context)
