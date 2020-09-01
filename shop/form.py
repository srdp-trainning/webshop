from django import forms
import re


class ReviewForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea, label="评论")


class DepositForm(forms.Form):
    money = forms.DecimalField(max_digits=10,decimal_places=2,label="充钱",
                               error_messages={'required':"不能为空", 'invalid':"格式错误"})

    # def clean_money(self):
    #     money = self.cleaned_data.get('money')
    #     try:
    #         money = float(money)
    #     except ValueError:
    #         raise forms.ValidationError("格式错误")
    #     if money < 0:
    #         raise forms.ValidationError("格式错误")
    #     if money > 10000:
    #         raise forms.ValidationError("冲太多了")
    #     return money


class ReplyForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea, label="回复")


class SearchForm(forms.Form):
    search = forms.CharField(label="搜索", required=False)

    def clean_search(self):
        raw_search = self.cleaned_data.get('search')
        if re.match(r'=', raw_search):
            raw_search = raw_search.replace('=', ' ')
        return raw_search


class PurchaseForm(forms.Form):
    number = forms.IntegerField(label="购买个数", error_messages={'invalid':"格式错误"})

    def clean_number(self):
        number = self.cleaned_data.get('number')
        if number < 0:
            raise forms.ValidationError("输入错误")
        return number