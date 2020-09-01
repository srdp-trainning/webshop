from django import forms
from account.models import *
import re
import hashlib

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, label="账号",
                               error_messages={'required': "请输入账号",
                                               'max_length': "账号长度不能大于20"})
    password = forms.CharField(widget=forms.PasswordInput,
                               max_length=30, label="密码",
                               error_messages={'required': "请输入密码",
                                               'max_length': "密码长度不能大于30"})
    # code = forms.CharField(max_length=20, label="验证码", error_messages={'required':"请输入验证码"})
    #
    #
    # def __init__(self, request, *args, **kwargs):
    #     self.request = request
    #     super(LoginForm, self).__init__(*args, **kwargs)
    #
    # def clean_code(self, request):
    #     raw_code = self.cleaned_data.get('code')
    #     if request.session.get('code',None) == None:
    #         raise forms.ValidationError("验证码过期")
    #     if raw_code != request.session.get('code'):
    #         raise forms.ValidationError("验证码错误")
    #     return raw_code

    def clean_username(self):
        row_username = self.cleaned_data.get('username')
        if not re.match(r'\w+$',row_username):
            raise forms.ValidationError("请输入合理的名字")
        result = UserAll.objects.filter(name=row_username)
        if not result:
            raise forms.ValidationError('用户名不存在')
        return row_username

    def clean_password(self):
        username = self.cleaned_data.get('username')
        result = UserAll.objects.filter(name=username)
        if not result:
             pass
        else:
            real_password = UserAll.objects.get(name=username).password
            row_password = self.cleaned_data['password']
            if not re.match(r'\w+$', row_password):
                raise forms.ValidationError("请输入合理的密码")
            if hashlib.sha1(row_password.encode('utf-8')).hexdigest() != real_password:
                raise forms.ValidationError("密码错误")
            return row_password


class RegisterForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput,
                               max_length=30, label="密码",
                               error_messages={'required': "请输入密码",
                                               'max_length': "密码长度不能大于30"})
    password2 = forms.CharField(widget=forms.PasswordInput,
                                max_length=30, label="再次输入密码",
                                error_messages={'required': "请输入密码",
                                                'max_length': "密码长度不能大于30"})
    class Meta:
        model = UserAll
        fields = ('email','name','identity')
        labels = {
            'email':"邮箱",
            'name':"姓名",
            'identity':"身份",
        }
        error_messages = {
            '__all__':{'required':"不能为空"},
            'email':{'invalid':"邮箱格式错误"}
        }

    def clean_name(self):
        row_username = self.cleaned_data['name']
        if not re.match(r'\w+$',row_username):
            raise forms.ValidationError("请输入合理的名字")
        result = UserAll.objects.filter(name=row_username)
        if result:
            raise forms.ValidationError('用户名已经存在')
        return row_username

    def clean_password1(self):
        row_password1 = self.cleaned_data['password1']
        if not re.match(r'\w+$', row_password1):
            raise forms.ValidationError("请输入合理的密码")
        return row_password1

    def clean_password2(self):
        try:
            password1 = self.cleaned_data.get('password1')
        except KeyError:
            raise forms.ValidationError("请输入合理的密码")
        else:
            row_password2 = self.cleaned_data.get('password2')
            if not re.match(r'\w+$', row_password2):
                raise forms.ValidationError("请输入合理的密码")
            if password1 != row_password2:
                raise forms.ValidationError("两次密码要一致")
            encrypt_password = hashlib.sha1(row_password2.encode('utf-8')).hexdigest()
            return encrypt_password

    def clean_email(self):
        row_email = self.cleaned_data['email']
        result = UserAll.objects.filter(email=row_email)
        if result:
            raise forms.ValidationError("邮箱已经注册")
        else:
            return row_email


class ResetForm(forms.Form):
    username = forms.CharField(max_length=20, label="账号",
                               error_messages={'required': "请输入账号",
                                               'max_length': "密码长度不能大于20"})

    def clean_username(self):
        row_username = self.cleaned_data['username']
        if not re.match(r'\w+$',row_username):
            raise forms.ValidationError("请输入合理的名字")
        result = UserAll.objects.filter(name=row_username)
        if not result:
            raise forms.ValidationError('用户名不存在')
        return row_username


class ChangeForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput,
                                max_length=30, label="密码",
                                error_messages={'required': "请输入密码",
                                                'max_length': "密码长度不能大于30"})
    password2 = forms.CharField(widget=forms.PasswordInput,
                                max_length=30, label="再次输入密码",
                                error_messages={'required': "请输入密码",
                                                'max_length': "密码长度不能大于30"})

    def clean_password1(self):
        row_password1 = self.cleaned_data['password1']
        if not re.match(r'\w+$', row_password1):
            raise forms.ValidationError("请输入合理的密码")
        return row_password1

    def clean_password2(self):
        try:
            password1 = self.cleaned_data.get('password1')
        except KeyError:
            raise forms.ValidationError("请输入合理的密码")
        else:
            row_password2 = self.cleaned_data['password2']
            if not re.match(r'\w+$', row_password2):
                raise forms.ValidationError("请输入合理的密码")
            if password1 != row_password2:
                raise forms.ValidationError("两次密码要一致")
            encrypt_password = hashlib.sha1(row_password2.encode('utf-8')).hexdigest()
            return encrypt_password