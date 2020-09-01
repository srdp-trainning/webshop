from django.db import models
from django.utils import timezone
from account.models import Seller,Customer
from django.shortcuts import reverse
import os
import uuid
import datetime
import random


def good_dictionary_path(instance, filename):
    type = filename.split('.')[-1]                          # get what type the photo is
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], type)  # generate a unique string
    return os.path.join(str(instance.owner.id),"image", filename)


def unique():
    time_now = datetime.datetime.now()
    year = time_now.year
    month = time_now.month
    day = time_now.day
    hour = time_now.hour
    minute = time_now.minute
    second = time_now.second
    return "good%d%d%d%d%d%d%d" % (year, month, day, hour, minute, second, random.randint(10, 99))

class Goods(models.Model):
    tags_choice = (
        ('clothes', "上衣"),
        ('shoes', "鞋子"),
        ('hat', "帽子"),
        ('trouser', "裤子"),
        ('underwear', "内衣")
    )
    fake_id = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    tags = models.CharField(max_length=12, choices=tags_choice, null=True)
    owner = models.ForeignKey(Seller, related_name='good_owner',on_delete=models.CASCADE)
    view = models.ImageField(upload_to=good_dictionary_path, blank=True)
    price = models.DecimalField(u'价格',decimal_places=2,max_digits=10)
    stock = models.PositiveIntegerField()
    created = models.DateTimeField(default=timezone.now)
    on_sale = models.BooleanField(default=False)
    detail_information = models.TextField()
    version_number = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class ShoppingCart(models.Model):
    customer = models.ForeignKey(Customer, related_name='owner',on_delete=models.CASCADE)
    good = models.ForeignKey(Goods, related_name='good_cart',on_delete=models.CASCADE)
    number = models.IntegerField(default=1)

    def __str__(self):
        return self.good.name

    class Meta:
        verbose_name_plural = "购物车"
        verbose_name = "购物车"


# save the newest revision for easily searching
class NewestGoods(models.Model):
    tags_choice = (
        ('clothes', "上衣"),
        ('shoes', "鞋子"),
        ('hat', "帽子"),
        ('trouser', "裤子"),
        ('underwear', "内衣")
    )
    fake_id = models.CharField(u'商品编号',max_length=100)
    name = models.CharField(u'商品名',max_length=50)
    tags = models.CharField(u'标签',max_length=12, choices=tags_choice, null=True)
    owner = models.ForeignKey(Seller, related_name='owner',
                              on_delete=models.CASCADE, verbose_name="所属商家")
    view = models.ImageField(upload_to=good_dictionary_path, blank=True, null=True)
    price = models.DecimalField(u'价格',decimal_places=2,max_digits=10)
    stock = models.PositiveIntegerField(u'库存')
    on_sale = models.BooleanField(u'是否上架?',default=False)
    detail_information = models.TextField(u'详细消息')
    newest_version = models.IntegerField(default=0)

    class Meta:
        verbose_name = "商品"
        verbose_name_plural = "商品"

    def get_absolute_url(self):                       # display for customer
        return reverse('shop:good_detail',kwargs={'fake_id':self.fake_id})

    def good_absolute_url(self):                      # display for seller
        return reverse('usage:detail',kwargs={'fake_id':self.fake_id})

    def owner_name(self):
        return self.owner.person.name

    def __str__(self):
        return self.name