from django.contrib import admin
from django.urls import path, include
from .views import products, product

app_name = 'mainapp'

urlpatterns = [
   path('', products, name='index'),
   path('category/<int:pk>/', products, name='category'),
   path('product/<int:pk>/', product, name='detail'),

]
