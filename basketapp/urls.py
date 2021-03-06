from django.contrib import admin
from django.urls import path, include
import basketapp.views as basketapp


app_name = 'basketapp'

urlpatterns = [
    path('', basketapp.basket, name='index'),
    path('add/<int:pk>/', basketapp.basket_add, name='add'),
    path('remove/<int:pk>/', basketapp.basket_remove, name='remove'),
]