from django import forms
# from tinymce.models import HTMLField
from shop.models import Goods, NewestGoods
from account.models import UserAll
import re


class NewGoodForm(forms.ModelForm):
    # content = HTMLField()
    view = forms.ImageField(label="商品主略览图",required=False)

    class Meta:
        model = NewestGoods
        fields = ('name', 'tags', 'price', 'stock')
        labels = {
            'name': "商品名",
            'tags': "商品标签",
            'price': "商品价格",
            'stock':"库存",
        }
        error_messages = {
            '__all__':{'required':"不能为空",'invalid':"格式错误"},
        }

    def clean_name(self):
        row_name = self.cleaned_data['name']
        if not re.match(r'\w+$',row_name):
            raise forms.ValidationError("请输入合理的名字")
        return row_name

    # def clean_price(self):
    #     price = self.cleaned_data.get('price')
    #     try:
    #         price = float(price)
    #     except ValueError:
    #         raise forms.ValidationError("格式错误")
    #     if price < 0:
    #         raise forms.ValidationError("格式错误")
    #     return price


class SellerInformationForm(forms.ModelForm):

    address = forms.CharField(max_length=50, label="商家地址",
                              error_messages={'required':"不能为空",
                                              'max_length':"最大长度为50"})
    phone = forms.CharField(max_length=15, label="联系方式",
                            error_messages={'required':"不能为空",
                                            'max_length':"最大长度为11"})

    class Meta:
        model = UserAll
        fields = ('avatar',)
        labels = {
            'avatar':"头像",
        }
        error_messages = {
            'avatar':{'invalid':"图片格式错误"},
        }


    def clean_phone(self):
        raw_phone = self.cleaned_data.get('phone')
        if len(raw_phone) != 11:
            raise forms.ValidationError("手机号必须11位")
        if not re.match(r'^\d+$', raw_phone):
            raise forms.ValidationError("手机号格式错误")
        return raw_phone



class CustomerInformationForm(forms.ModelForm):
    class Meta:
        model = UserAll
        fields = ('avatar',)
        labels = {
            'avatar':"头像",
        }
        error_messages = {
            'avatar':{'invalid':"图片格式错误"},
        }

