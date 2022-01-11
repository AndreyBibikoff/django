from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from adminapp.forms import ShopUserAdminEditForm, ProductCategoryEditForm, ProductEditForm
from authapp.forms import ShopUserRegisterForm

from authapp.models import ShopUser
from mainapp.models import Product, ProductCategory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

class UsersListView(ListView):
    model = ShopUser
    template_name = "adminapp/users.html"
    context_object_name = 'objects'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UsersListView, self).get_context_data(**kwargs)
        context['title'] = 'админка/пользователи'
        return context


class UserCreateView(CreateView):
    model = ShopUser
    template_name = 'adminapp/user_create.html'
    success_url = reverse_lazy('admin_staff:users')
    form_class = ShopUserRegisterForm

# @user_passes_test(lambda u: u.is_superuser)
# def user_create(request):
#     title = 'пользователи/cоздание'
#
#     if request.method == 'POST':
#         user_form = ShopUserRegisterForm(request.POST, request.FILES)
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('admin_staff:users'))
#
#     else:
#         user_form = ShopUserRegisterForm()
#
#     context = {
#         'title': title,
#         'user_form': user_form,
#     }
#
#     return render(request, 'adminapp/user_create.html', context)


class UserEditView(UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin_staff:users')
    # fields = '__all__'
    form_class = ShopUserAdminEditForm

# @user_passes_test(lambda u: u.is_superuser)
# def user_update(request, pk):
#     title = 'пользователи/редактирование'
#
#     edit_user = get_object_or_404(ShopUser, pk=pk)
#
#     if request.method == 'POST':
#         edit_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
#
#         if edit_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('admin_staff:user_update', args=[edit_user.pk]))
#     else:
#         edit_form = ShopUserAdminEditForm(instance=edit_user)
#
#     context = {
#         'title': title,
#         'user_form': edit_form,
#     }
#
#     return render(request, 'adminapp/user_update.html', context)


class UserDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    context_object_name = 'user_to_delete'
    success_url = reverse_lazy('admin_staff:users')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()

        return HttpResponseRedirect(self.get_success_url())

@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    title = 'пользователи/удаление'

    user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse('admin_staff:users'))

    context = {
        'title': title,
        'user_to_delete': user,
    }

    return render(request, 'adminapp/user_delete.html', context)


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    title = 'админка/категории'

    all_categories = ProductCategory.objects.all()

    context = {
        'title': title,
        'objects': all_categories,
    }

    return render(request, 'adminapp/categories.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_create(request):
    title = 'категории/cоздание'

    if request.method == 'POST':
        category_form = ProductCategoryEditForm(request.POST, request.FILES)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('admin_staff:categories'))

    else:
        category_form = ProductCategoryEditForm()

    context = {
        'title': title,
        'category_form': category_form,
    }

    return render(request, 'adminapp/category_create.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_update(request, pk):
    title = 'категория/редактирование'

    edit_category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        edit_form = ProductCategoryEditForm(request.POST, request.FILES, instance=edit_category)

        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin_staff:category_update', args=[edit_category.pk]))
    else:
        edit_form = ProductCategoryEditForm(instance=edit_category)

    context = {
        'title': title,
        'category_form': edit_form,
    }

    return render(request, 'adminapp/category_update.html', context)

@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk):
    title = 'категория/удаление'

    delete_category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        delete_category.delete()
        return HttpResponseRedirect(reverse('admin_staff:categories'))

    context = {
        'title': title,
        'category_to_delete': delete_category,
    }

    return render(request, 'adminapp/category_delete.html', context)

@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    title = 'админка/продукт'

    category = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category__pk=pk).order_by('name')

    context = {
        'title': title,
        'category': category,
        'objects': products_list,
    }

    return render(request, 'adminapp/products.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_create(request, pk):
    title = 'продукт/cоздание'
    category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('admin_staff:products', args=[pk]))

    else:
        product_form = ProductEditForm(initial={'category': category})

    context = {
        'title': title,
        'update_form': product_form,
    }

    return render(request, 'adminapp/product_create.html', context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'

# @user_passes_test(lambda u: u.is_superuser)
# def product_read(request, pk):
#     pass


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    title = 'продукт/редактирование'

    edit_product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        edit_form = ProductEditForm(request.POST, request.FILES, instance=edit_product)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin_staff:product_update', args=[edit_product.pk]))

    else:
        edit_form = ProductEditForm(instance=edit_product)

    context = {
        'title': title,
        'update_form': edit_form,
        'category': edit_product.category
    }

    return render(request, 'adminapp/product_create.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    title = 'продукт/удаление'

    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.delete()
        return HttpResponseRedirect(reverse('admin_staff:products', args=[product.category.pk]))

    context = {
        'title': title,
        'product_to_delete': product,
    }

    return render(request, 'adminapp/product_delete.html', context)