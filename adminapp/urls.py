from django.contrib import admin
from django.urls import path, include

import adminapp.views as adminapp
from django.views.decorators.cache import cache_page

app_name = 'authapp'

urlpatterns = [

    path('users/create/', adminapp.UserCreateView.as_view(), name='user_create'),
    path('users/read/', cache_page(3600)(adminapp.UsersListView.as_view()), name='users'),
    #    path('users/read/<int:page>/', adminapp.users, name='page'),
    path('users/update/<int:pk>/', adminapp.UserEditView.as_view(), name='user_update'),
    path('users/delete/<int:pk>/', adminapp.UserDeleteView.as_view(), name='user_delete'),

    path('categories/create/', adminapp.category_create, name='category_create'),
    path('categories/read/', adminapp.categories, name='categories'),
    path('categories/update/<int:pk>/', adminapp.category_update, name='category_update'),
    path('categories/delete/<int:pk>/', adminapp.category_delete, name='category_delete'),

    path('products/create/category/<int:pk>/', adminapp.product_create, name='product_create'),
    path('products/read/category/<int:pk>/', adminapp.products, name='products'),
    path('products/read/<int:pk>/', adminapp.ProductDetailView.as_view(), name='product_read'),
    path('products/update/<int:pk>/', adminapp.product_update, name='product_update'),
    path('products/delete/<int:pk>/', adminapp.product_delete, name='product_delete'),

]
