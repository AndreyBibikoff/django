from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from basketapp.models import Basket
from mainapp.models import Product
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def basket(request):
    basket = []
    title = 'GeekShop - Корзина'
    basket_items = Basket.objects.filter(user=request.user)
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
    context = {
        'title': title,
        'basket': basket,
        'basket_items': basket_items,

    }
    return render(request, 'basketapp/basket.html', context)

@login_required
def basket_add(request, pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:detail', args=[pk]))

    product = get_object_or_404(Product, pk=pk)

    basket = Basket.objects.filter(user=request.user, product=product).first()

    if not basket:
        basket = Basket(user=request.user, product=product)

    basket.quantity += 1
    basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def basket_remove(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk)
    basket_record.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
