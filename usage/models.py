from django.db import models
from django.utils import timezone
from account.models import Customer, Seller, UserAll
from shop.models import Goods, NewestGoods
import uuid
from django.shortcuts import reverse


class Reviews(models.Model):
    body = models.TextField(u'内容')
    date = models.DateTimeField(u'时间',default=timezone.now)
    writer = models.ForeignKey(UserAll, related_name='review_writer',on_delete=models.CASCADE)
    good = models.ForeignKey(NewestGoods, related_name='review_good',on_delete=models.CASCADE)
    # where there is a reply,for a review, the reply_id equal to the id of review
    reply_id = models.IntegerField(default=0)

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = "评论"

    def writer_name(self):
        return self.writer.name


class Order(models.Model):
    code = models.CharField(u'单号',max_length=50)
    sender = models.ForeignKey(Customer, related_name='order_sender',
                               on_delete=models.CASCADE, verbose_name="购买方")
    receiver = models.ForeignKey(Seller, related_name='order_receiver',
                                 on_delete=models.CASCADE, verbose_name="商家")
    good = models.ForeignKey(Goods,related_name= 'order_good',
                             on_delete=models.CASCADE, verbose_name="商品")
    date = models.DateTimeField(u'时间',default=timezone.now)
    status = models.BooleanField(u'状态',default=False)
    number = models.IntegerField(u'购买个数',default=1)

    class Meta:
        verbose_name = "订单"
        verbose_name_plural = "订单"

    def sender_name(self):
        return self.sender.person.name

    def receiver_name(self):
        return self.receiver.person.name

    def good_name(self):
        return self.good.name

    def get_order_url(self):
        return reverse('shop:order-detail',kwargs={'code':self.code})

    def __str__(self):
        return self.code