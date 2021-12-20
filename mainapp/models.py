from django.db import models


# Create your models here.

class ProductCategory(models.Model):
    category_name = models.CharField(verbose_name='Наименование категории', max_length=64, unique=True)
    description = models.TextField(verbose_name='Описение', blank=True)

    def __str__(self):
        return f'{self.category_name} | {self.description}'


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Наименование продукта', max_length=64)
    image = models.ImageField(upload_to='products_image', blank=True)
    short_descript = models.CharField(verbose_name='Краткое описание', max_length=128, blank=True)
    description = models.TextField(verbose_name='Описение продукта', blank=True)
    price = models.DecimalField(verbose_name='Стоимость', max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(verbose_name='Количество', default=0)

    def __str__(self):
        return f'{self.name} - ({self.category.category_name})'

