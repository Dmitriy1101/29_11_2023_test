from django.db import models
from django.conf import settings
import stripe


class Item(models.Model):
    '''
        Django Модель Item с полями (name, description, price)
        test product id = prod_P5tzjkTzI0EiUe
    '''

    CURRENCYS = [
        ("USD", "USA"),
        ("RUB", "RUB"),
        ("EUR", "EUR"),
    ]
    name = models.CharField('Название', unique = True, null = False)
    description = models.TextField('Описание', blank = True)
    price = models.DecimalField('Цена', default= 0,  max_digits=5, decimal_places=2)
    currency = models.CharField('Валюта', choices = CURRENCYS, default = 'USD')
    stripe_product_id = models.CharField(editable = False, blank = True)
    stripe_price_id = models.CharField(editable = False, blank = True)


    def save(self, *args, **kwargs):
        stripe.api_key = settings.STRIPE_TEST_SKEY
        price = int(self.price * 100)
        prod = stripe.Product.create(name = self.name, default_price_data = {'currency' : self.currency, 'unit_amount_decimal' : price})
        self.stripe_product_id = prod['id']
        self.stripe_price_id = prod['default_price']
        return super().save(*args, **kwargs)


    def __str__ (self):
        return f'item: {str(self.name)}, price:{str(self.price)}'


    class Meta:
        verbose_name = 'Тоовар'
        verbose_name_plural = 'Товары'



class Order(models.Model):
    '''
        Модель Order, в которой можно объединить несколько Item 
        и сделать платёж в Stripe 
        на содержимое Order c общей стоимостью всех Items
    '''

    item = models.ManyToManyField(Item, related_name='orders')
    total_price = models.DecimalField('Цена', default = 0,  max_digits=7, decimal_places=2)
    order_details = models.JSONField('Спецификация', default = dict)


    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'