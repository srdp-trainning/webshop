from django.shortcuts import render,HttpResponse,redirect,reverse
from account.form import *
from account.models import *
from django.core.mail import send_mail
import code,random
from io import BytesIO


# a decorator to check if login
def login_required(func):
    def wrapper(request):
        status = request.session.get('status',None)
        if status:
            decorated_func = func(request)
            return decorated_func
        else:
            return render(request,'forbidden.html')
    return wrapper


# check whether login or not
def check_code(request):
    code_str = request.session.get('code', None)
    real_code = request.POST.get('code')
    if code_str == real_code or code_str.lower() == real_code:
        return True
    else:
        return False


# create a code and save the code-image in cache
def code_img(request):
    f = BytesIO()
    image,str = code.create()
    request.session['code'] = str
    request.session.set_expiry(120)
    image.save(f, 'png')
    return HttpResponse(f.getvalue())


# handel login logic
def login(request):
    status = request.session.get('status',None)
    if status:                  # avoid repeat login
        return redirect(reverse('home'))
    else:
        if request.method == 'GET':
            login_form = LoginForm()
            return render(request, 'account/login.html', {'form': login_form})
        if request.method == 'POST':
            if check_code(request):
                login_form = LoginForm(request.POST)
                if login_form.is_valid():
                    username = login_form.cleaned_data['username']
                    if Seller.objects.filter(store_status=False, person__name=username):
                        return HttpResponse("你被封号了，哈哈哈")
                    request.session['status'] = True
                    request.session['name'] = username
                    request.session.set_expiry(86400)   # set 1 day as expiry date
                    request.session.set_expiry(0)       # out of date when close the browser
                    print(username+'login!')
                    return redirect('/')
                else:
                    return render(request,'account/login.html',{'form': login_form})
            else:
                login_form = LoginForm(request.POST)
                dict = {'form':login_form, 'check':"验证码错误"}
                return render(request,'account/login.html',dict)


# handle the register logic
def register(request):
    if request.method == 'GET':
        register_form = RegisterForm()
        return render(request, 'account/register.html', {'form':register_form})
    if request.method == 'POST':
        register_form = RegisterForm()
        if check_code(request):
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                username = register_form.cleaned_data.get('name')
                email = register_form.cleaned_data.get('email')
                password = register_form.cleaned_data.get('password2')
                identity = register_form.cleaned_data.get('identity')
                new_user = UserAll(name=username, email=email,
                                   password=password, identity=identity)
                new_user.save()
                if new_user.identity == 'c':
                    Customer.objects.create(person=new_user)
                else:
                    Seller.objects.create(person=new_user)
                return redirect(reverse('account:login'))
            else:
                return render(request, 'account/register.html', {'form': register_form})
        else:
            dict = {'form': register_form, 'check': "验证码错误"}
            return render(request, 'account/register.html', dict)


# handle sending email logic
def password_reset(request):
    if request.method == 'GET':
        reset_form = ResetForm()
        return render(request,'account/reset.html',{'form':reset_form})
    if request.method == 'POST':
        reset_form = ResetForm()
        if check_code(request):
            reset_form = ResetForm(request.POST)
            if reset_form.is_valid():
                username = reset_form.cleaned_data.get('username')
                email = UserAll.objects.get(name=username).email
                title = "修改密码"
                secret1 = str(uuid.uuid4())
                body = "点击下面链接修改密码:http://127.0.0.1:8000/home/modify/?code={},".format(secret1)
                request.session['secret'] = secret1
                request.session['name'] = username
                request.session.set_expiry(60)
                print('send email to',username)
                send_mail(subject=title, message=body, from_email='cyx',
                          recipient_list=[email])
                return render(request, 'account/success_send.html')
        else:
            dict = {'form': reset_form, 'check': "验证码错误"}
            return render(request, 'account/reset.html', dict)


# handle the modify password logic
def password_change(request):
    code = request.GET.get('code')
    if code == request.session.get('secret', None):  # check code send by url
        if request.method == 'GET':
            change_form = ChangeForm()
            return render(request, 'account/reset_revise.html',{'form':change_form})
        if request.method == 'POST':
            change_form = ChangeForm(request.POST)
            if change_form.is_valid():
                username = request.session.get('name')
                user = UserAll.objects.get(name=username)
                new_password = change_form.cleaned_data['password2']
                user.password = new_password
                user.save()
                return redirect(reverse('account:login'))
            else:
                return render(request, 'account/reset_revise.html', {'form': change_form})
    else:
        return redirect(reverse('account:login'))



