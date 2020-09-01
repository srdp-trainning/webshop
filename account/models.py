from django.db import models
import os
import uuid
from django.utils.safestring import mark_safe


def user_dictionary_path(instance, filename):
    ext = filename.split('.')[-1]                          # get what type the photo is
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)  # generate a unique string
    # return the whole path ,include value of id
    return os.path.join(str(instance.id), "avatar", filename)


class UserAll(models.Model):
    seller = 's'
    customer = 'c'
    identity_choice = (
        (seller, "商家"),
        (customer, "买家")
    )
    name = models.CharField(u'姓名',max_length=20)
    password = models.TextField()
    email = models.EmailField(u'邮箱')
    avatar = models.ImageField(u'头像',blank=True, upload_to=user_dictionary_path,
                               default='timg.jpg')
    identity = models.CharField(u'身份',max_length=1, choices=identity_choice,null=True)

    class Meta:
        verbose_name = "所有用户"
        verbose_name_plural = "所有用户"

    def __str__(self):
        return self.name
    
    def img(self):
        return mark_safe('<img src="%s" width="50px"/>' % self.avatar.url)


class Customer(models.Model):
    person = models.OneToOneField(UserAll, on_delete=models.CASCADE,verbose_name="用户")
    fund = models.DecimalField(u'余额', default=0, decimal_places=2,max_digits=10)

    def __str__(self):
        return self.person.name

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"


class Seller(models.Model):
    person = models.OneToOneField(UserAll, on_delete=models.CASCADE, verbose_name="商家")
    phone = models.CharField(u'电话',max_length=50)
    fund = models.DecimalField(u'余额',default=0,decimal_places=2,max_digits=10)
    store_status = models.BooleanField(u'商店状态',default=True)
    address = models.CharField(u'地址',max_length=40,blank=True)

    def __str__(self):
        return self.person.name

    class Meta:
        verbose_name = "商家"
        verbose_name_plural = "商家"
