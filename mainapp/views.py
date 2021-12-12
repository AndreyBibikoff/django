from django.shortcuts import render


# Create your views here./
def products(request):
    title = 'geekshop - каталог'
    links_menu = [
        {'href': '#', 'name': 'все'},
        {'href': '#', 'name': 'дом'},
        {'href': '#', 'name': 'офис'},
        {'href': '#', 'name': 'модерн'},
        {'href': '#', 'name': 'классика'},
    ]
    related_products = [
        {'name': 'лампа', 'img_link': '/static/geekshop/img/product-11.jpg', 'href': '#'},
        {'name': 'стул', 'img_link': '/static/geekshop/img/product-21.jpg', 'href': '#'},
        {'name': 'торшер', 'img_link': '/static/geekshop/img/product-31.jpg', 'href': '#'},
    ]
    context = {
        'title': title,
        'links_menu': links_menu,
        'related_products': related_products,
    }
    return render(request, 'mainapp/products.html', context=context)
