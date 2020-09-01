from django.shortcuts import render,redirect,HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse

from usage.models import *
from shop.models import *
from account.views import login_required
from django.conf import settings
from django.db.models import Q,F
from shop.form import *
import logging
import redis
from account.form import ChangeForm
r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT,
                      db=settings.REDIS_DB,password=settings.REDIS_PASSWORD)


# 生成一个当前文件名命名为命名的logger实例
# logger = logging.getLogger(__name__)
collect_log = logging.getLogger('collect')


# use redis to show most-viewed good
def most_viewed_good():
    good_ranking = r.zrange('good_ranking', 0, -1, desc=True)[:3]
    good_ranking_ids = [int(id) for id in good_ranking]
    most_viewed = list(NewestGoods.objects.filter(id__in=good_ranking_ids))
    most_viewed.sort(key=lambda x: good_ranking_ids.index(x.id))
    return most_viewed


def page_division(request, obj):
    paginator = Paginator(obj, 3)
    page = request.GET.get('page', 1)
    try:
        current_page = paginator.page(page)
        list_obj = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        list_obj = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        list_obj = current_page.object_list
    return list_obj,current_page


# home page
def home(request):
    collect_log.info("url:%s method:%s" %(request.path, request.method))
    username = request.session.get('name',None)
    status = request.session.get('status',None)
    most_viewed = most_viewed_good()
    if request.method == 'GET':
        if status:
            user_identity = UserAll.objects.get(name=username).identity
            if user_identity == 'c':
                form = SearchForm()
                return render(request, 'shop/home_c.html', locals())
            else:
                return render(request,'shop/home_s.html',locals())
        else:
            return render(request,'shop/home_c.html',{'most_viewed':most_viewed})
    if request.method == 'POST':
        if request.POST.get('logout'):
            collect_log.info("%s logout!" %(username ))
            request.session.flush()
            return redirect('/')
        if request.POST.get('searching'):
            search_form = SearchForm(request.POST)
            if search_form.is_valid():
                search = search_form.cleaned_data.get('search')
                # search by name and tags
                goods = NewestGoods.objects.filter((Q(name__icontains=search)|Q(tags__icontains=search))&Q(on_sale=True))
                if goods:
                    list_goods,current_page = page_division(request, goods)
                    return render(request, 'shop/good_list.html',{'goods':list_goods,'page':current_page})
                else:
                    return render(request, 'empty_good.html')
            else:
                render(request,'shop/home_s.html',locals())


# to show all the newest goods
def good_list(request):
    goods = NewestGoods.objects.all().filter(on_sale=True)
    list_good,current_page = page_division(request, goods)
    return render(request,'shop/good_list.html',{'goods':list_good,'page':current_page})


def review_display(fake_id):
    reviews = Reviews.objects.filter(good__fake_id=fake_id, reply_id=0)
    review_dict = {}
    for i in reviews:
        # in dictionary, each key was a review and the correspond value is a list contain reply
        review_dict[i] = [temp for temp in Reviews.objects.filter(reply_id=i.id)]
    return review_dict


def good_detail(request, fake_id):
    username = request.session.get('name',None)
    status = request.session.get('status',None)
    good_new = Goods.objects.filter(fake_id=fake_id).order_by('-version_number')[0]
    try:                                                 # avoid getting an non-existent url
        good = NewestGoods.objects.get(fake_id=fake_id)
    except NewestGoods.DoesNotExist:
        return render(request, 'empty_good.html')
    if request.method == 'GET':
        # record numbers of views
        # total_view = r.incr("good:{}:views".format(good.id))
        # r.zincrby('good_ranking', good.id, 1)
        # avoid repeat add in shopping_cart
        if ShoppingCart.objects.filter(good__fake_id=fake_id):
            in_cart = True
        else:
            in_cart = False
        # if this people doesn't login, he or she can't see the content under control of status
        review_form = ''
        try:
            customer = Customer.objects.get(person__name=username)
            if Order.objects.filter(good__fake_id=fake_id, status=True, sender=customer):
                review_form = ReviewForm()
        except Customer.DoesNotExist:
            customer_yes = False
        else:
            status = True
            customer_yes = True
        dict = {'good': good, 'status': status, 'form': review_form,'customer_yes':customer_yes,
                'in_cart': in_cart, 'reviews': review_display(fake_id), 'total_views':''}
        return render(request, 'shop/good_detail.html', dict)
    if request.method == 'POST':
        customer = Customer.objects.filter(person__name=username)[0]
        if request.POST.get('save_in'):  # save in shopping_cart
            ShoppingCart.objects.create(customer=customer, good=good_new)  # add in shopping_cart
            return render(request, 'message.html', {'message':"存入购物车成功", 'good':good})
        if request.POST.get('review'):  # 1 level review
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                user = UserAll.objects.get(name=username)
                review = review_form.cleaned_data.get('body')
                Reviews.objects.create(writer=user, good=good, body=review)
            return redirect(reverse('shop:good_detail', kwargs={'fake_id':fake_id}))


def good_purchase(request, fake_id):
    username = request.session.get('name')
    try:
        customer = Customer.objects.get(person__name=username)
    except Customer.DoesNotExist:
        return redirect(reverse('home'))
    try:
        good = NewestGoods.objects.get(fake_id=fake_id)
        good_new = Goods.objects.filter(fake_id=fake_id).order_by('-version_number')[0]
    except NewestGoods.DoesNotExist:
        return render(request, 'empty_good.html')
    if request.method == 'GET':
        number_form = PurchaseForm(initial={'number':1})
        return render(request, 'shop/order_number.html',{'good':good,'form':number_form,'user':customer})
    if request.method == 'POST':   # buy it
        number_form = PurchaseForm(request.POST)
        if number_form.is_valid():
            number = number_form.cleaned_data.get('number')
            price = good.price * number
            if customer.fund >= price:
                if good.stock - number >= 0:
                    customer.fund -= price
                    customer.save()
                    good_new.stock -= number
                    good_new.save()
                    good.stock -= number
                    good.save()
                    Order.objects.create(sender=customer, receiver=good.owner, good=good_new,
                                         number=number,code=uuid.uuid1())
                    return render(request, 'message.html', {'message': "下单成功", 'deposit': False,
                                                            'good': good})
                else:
                    return render(request, 'message.html', {'message': "库存不足", 'deposit': False,
                                                            'good': good})
            else:
                return render(request, 'message.html', {'message': "余额不足", 'deposit': True,
                                                        'good': good})
        else:
            return render(request, 'shop/order_number.html', {'good':good, 'form':number_form, 'user':customer})


# display shopping_cart
@login_required
def my_cart(request):
    username = request.session.get('name')
    user = UserAll.objects.get(name=username)
    if user.identity == 's':
        return redirect('/')
    if request.method == 'GET':
        shopping_cart = ShoppingCart.objects.filter(customer=user.customer)
        return render(request, 'shop/shopping-cart.html', {'shopping_cart':shopping_cart })
    if request.method == 'POST':
        sum = 0
        shopping_cart = ShoppingCart.objects.filter(customer=user.customer)
        try:
            for i in request.POST.getlist('good_list'):
                one_cart = ShoppingCart.objects.get(id=i)
                good = one_cart.good  # search the good through shopping_cart table
                price = good.price
                number = int(request.POST.get(i))
                if number < 0 :
                    return render(request, 'shop/shopping-cart.html', {'shopping_cart':shopping_cart,
                                                                       'error':"个数不能小于0"})
                if good.stock < number:
                    return render(request, 'message.html', {'message': "库存不足", 'deposit': False,
                                                            'good': good})
                good.stock -= number
                good.save()
                sum += price * number
                if user.customer.fund < sum:
                    return render(request, 'message.html', {'message': "余额不足",
                                                            'deposit': True})
                else:
                    Order.objects.create(good=good, sender=user.customer,code=uuid.uuid1(),
                                         receiver=good.owner, number=number)
                shopping_cart.filter(id=i).delete()
        except TypeError:
            return redirect(reverse('shop:cart'))
        return HttpResponse("成功<a href=/>返回主页<a>")


@login_required
def deposit(request):
    username = request.session.get('name')
    user = UserAll.objects.get(name=username)
    customer = Customer.objects.get(person=user)
    if request.method == 'GET':
        fund = customer.fund
        deposit_form = DepositForm()
        return render(request, 'shop/deposit.html', {'form':deposit_form,'fund':fund})
    if request.method == 'POST':
        deposit_form = DepositForm(request.POST)
        fund = customer.fund
        if deposit_form.is_valid():
            deposit = deposit_form.cleaned_data['money']
            customer.fund += deposit
            customer.save()
            return render(request, 'shop/deposit.html', {'message':"充值成功",'form':deposit_form,'fund':fund})
        else:
            return render(request, 'shop/deposit.html', {'message':"充值失败",'form':deposit_form,'fund':fund})


def reply(request, fake_id, review_id):
    username = request.session.get('name',None)
    if not username:
        return redirect(reverse('account:login'))
    else:
        user = UserAll.objects.get(name=username)
    try:
        good = NewestGoods.objects.get(fake_id=fake_id)
        review = Reviews.objects.filter(reply_id=0).get(id=review_id)
    except NewestGoods.DoesNotExist:
        return render(request, 'empty_good.html')
    except Reviews.DoesNotExist:
        return HttpResponse("评论不存在，可能删除了")
    else:
        if request.method == 'GET':
            reply_form = ReplyForm()
            return render(request, 'shop/reply.html',{'form':reply_form})
        if request.method == 'POST': # 2 level review
            reply_form = ReplyForm(request.POST)
            if reply_form.is_valid():
                body = reply_form.cleaned_data.get('body')
                Reviews.objects.create(good=good, reply_id=review.id, body=body, writer=user)
                return redirect(reverse('shop:good_detail', kwargs={'fake_id':fake_id}))
            else:
                return render(request, 'shop/reply.html', {'form': reply_form})


@login_required
def shopping_detail(request):
    username = request.session.get('name')
    try:
        customer = Customer.objects.get(person__name=username)
    except Customer.DoesNotExist:
        return render(request, 'forbidden.html')
    else:
        code = request.GET.get('code',None)
        if code:
            try:
                order = Order.objects.get(code=code)
            except Order.DoesNotExist:
                return HttpResponse("找不到订单")
            else:
                if order.sender.person.name != username or order.status == True:
                    return render(request, 'forbidden.html')
                money = order.good.price * int(order.number)
                Customer.objects.filter(order_sender__code=code).update(fund=(F('fund')+money))
                Order.objects.filter(code=code).delete()
                return redirect(reverse('shop:shopping_detail'))
        else:
            orders = Order.objects.filter(sender=customer)
            list_order,current_page = page_division(request, orders)
            return render(request, 'shop/shopping_order.html', {'orders':list_order,'page':current_page})


def order_detail(request, code):
    if request.session.get('status',None):
        order = Order.objects.get(code=code)
        username = request.session.get('name')
        user = UserAll.objects.get(name=username)
        return render(request, 'shop/order_detail.html', {'order':order,'user':user})
    else:
        return redirect(reverse('home'))


@login_required
def password_change(request):
    username = request.session.get('name')
    if request.method == 'GET':
        reset_form = ChangeForm()
        return render(request, 'shop/reset-password.html',{'form':reset_form})
    if request.method == 'POST':
        reset_form = ChangeForm(request.POST)
        if reset_form.is_valid():
            user = UserAll.objects.get(name=username)
            new_password = reset_form.cleaned_data['password2']
            user.password = new_password
            user.save()
            return HttpResponse("修改成功<a href=/>返回主页</a><br>")
        else:
            return render(request, 'shop/reset-password.html',{'form':reset_form})
