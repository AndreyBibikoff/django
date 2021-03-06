from django.shortcuts import render

from basketapp.models import Basket
from mainapp.models import Product


def index(request):
    title = 'geekshop - главная'
    products = Product.objects.all()

    context = {
        'title': title,
        'products': products,
    }
    return render(request, 'geekshop/index.html', context=context)


def contacts(request):
    title = 'geekshop - контакты'
    contacts_cards = [
        {'City': 'Москва', 'phone': '+7-888-888-8888', 'Email': 'moscow@geekshop.ru', 'adress': 'В пределах МКАД'},
        {'City': 'Санкт-Петербург', 'phone': '+7-777-777-7777', 'Email': 'spb@geekshop.ru', 'adress': 'В пределах КАД'},
        {'City': 'Казань', 'phone': '+7-111-111-1111', 'Email': 'kzn@geekshop.ru', 'adress': 'В пределах города'},
   ]
    context = {
        'title': title,
        'contacts_cards': contacts_cards,
    }
    return render(request, 'geekshop/contacts.html', context=context)

