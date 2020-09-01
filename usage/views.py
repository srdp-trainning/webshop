from django.shortcuts import render,redirect,reverse
from shop.models import *
from usage.models import Order
from usage.form import *
from account.views import login_required
from account.models import UserAll,Seller
from shop.views import page_division
from PIL import Image
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
# from shop.views import r
import uuid

# a decorate to check customer or seller
def seller_only(func):
    def wrapper(request, fake_id):
        username = request.session.get('name',None)
        try:                                            # to check if login
            user = UserAll.objects.get(name=username)
        except UserAll.DoesNotExist:
            return redirect(reverse('account:login'))
        else:
            if user.identity != 's':
                return render(request,'forbidden.html')
            else:
                decorated_func = func(request, fake_id)
                return decorated_func
    return wrapper


@login_required
def new_good(request):
    username = request.session.get('name')
    user = UserAll.objects.get(name=username)
    if user.identity == 'c':
        return render(request, 'forbidden.html')
    seller = Seller.objects.get(person=user)
    if request.method == 'GET':
        good_form = NewGoodForm()
        return render(request, 'usage/new-good.html', {'form':good_form})
    if request.method == 'POST':
        good_form = NewGoodForm(request.POST,request.FILES)
        content = request.POST.get('content')
        if good_form.is_valid():
            fake_id = uuid.uuid1()
            view = good_form.cleaned_data.get('view')
            name = good_form.cleaned_data.get('name')
            tags = good_form.cleaned_data.get('tags')
            price = good_form.cleaned_data.get('price')
            stock = good_form.cleaned_data.get('stock')
            good = Goods(name=name, tags=tags, price=price, stock=stock,fake_id=fake_id,
                         view=view, detail_information=content,owner=seller)
            new = NewestGoods(name=name, tags=tags, price=price, stock=stock,owner=seller,
                              view=view, detail_information=content, fake_id=fake_id)
            if request.POST.get('on_sale'):
                good.on_sale = True
                new.on_sale = True
            good.save()
            new.save()
            print("new good",good.name)
            return redirect(reverse('usage:list'))
        else:
            return render(request,'usage/new-good.html',{'form':good_form})


# handle the logic of listing all the good seller has
@login_required
def my_store(request):
    username = request.session.get('name')
    user = UserAll.objects.get(name=username)
    if user.identity == 'c':
        return render(request, 'forbidden.html')
    if request.method == 'GET':
        seller = Seller.objects.get(person=user)
        goods = seller.owner.all()
        return render(request, 'usage/good-list.html', {'name':username,'goods':goods})
    if request.method == 'POST':
        return redirect(reverse('usage:list'))


# handle logic of displaying detail information for a good
@ seller_only
def my_good(request, fake_id):
    username = request.session.get('name',None)
    if request.method == 'GET':
        try:
            newest_good = NewestGoods.objects.get(fake_id=fake_id)
        except NewestGoods.DoesNotExist:
            return render(request, 'empty_good.html')
        else:
            seller = newest_good.owner.person
            if seller.name != username:
                return redirect(reverse('shop:good_detail',kwargs={'fake_id': fake_id}))
            else:
                return render(request, 'usage/good-detail.html',{'good':newest_good})
    if request.method == 'POST':
        return redirect(reverse('usage:revise', kwargs={'fake_id': fake_id}))


#  handle the logic of revise a good
@seller_only
def good_revise(request, fake_id):
    username = request.session.get('name')
    user = UserAll.objects.get(name=username)
    good = NewestGoods.objects.all().get(fake_id=fake_id)
    if user.id != good.owner.person.id:
        return redirect(reverse('shop:good_detail',kwargs={'fake_id': fake_id}))
    else:
        if request.method == 'GET':
            init = {'name': good.name, 'tags': good.tags, 'stock':good.stock,
                    'price': good.price,'detail_information':good.detail_information}
            good_form = NewGoodForm(initial=init)
            return render(request, 'usage/good-revise.html',{'form': good_form,'good': good,
                                                             'detail_information':good.detail_information})
        if request.method == 'POST':
            good_form = NewGoodForm(request.POST, request.FILES)
            if request.POST.get('delete'):
                if Order.objects.filter(good__fake_id=fake_id,status=False):
                    return render(request, 'usage/order_handle.html',{'message':"你还有相关订单未处理"})
                NewestGoods.objects.filter(fake_id=fake_id).delete()
                Goods.objects.filter(fake_id=fake_id).delete()
                r.delete("good:{}:views".format(good.id))
                return redirect(reverse('usage:list'))
            if good_form.is_valid():
                version_number = good.newest_version + 1
                fake_id = good.fake_id
                view = good_form.cleaned_data.get('view')
                name = good_form.cleaned_data.get('name')
                tags = good_form.cleaned_data.get('tags')
                price = good_form.cleaned_data.get('price')
                stock = good_form.cleaned_data.get('stock')
                content =request.POST.get('content')
                newest = NewestGoods.objects.get(fake_id=fake_id)
                updated = Goods(view=view, name=name, tags=tags, detail_information=content,
                                price=price, stock=stock, version_number=version_number,
                                fake_id=fake_id)
                newest.newest_version = version_number
                newest.view = view
                newest.name = name
                newest.tags = tags
                newest.detail_information = content
                newest.price = price
                newest.stock = stock
                if request.POST.get('update'):
                    newest.on_sale = False
                    good.on_sale = False
                if request.POST.get('on_sale'):
                    newest.on_sale = True
                    good.on_sale = True
                updated.owner = Seller.objects.get(person=user)
                updated.save()
                newest.save()
                print("item {} revise".format(good.id))
                return redirect(reverse('usage:list'))
            else:
                return render(request, 'usage/good-revise.html', {'form':good_form,'good':good})


# display the detail personal information
@login_required
def information_view(request):
    username = request.session.get('name')
    user=UserAll.objects.get(name=username)
    if user.identity == 'c':
        fund = user.customer.fund
    if user.identity == 's':
        phone = user.seller.phone
        fund = user.seller.fund
        address = user.seller.address
    return render(request, 'usage/information-view.html',locals())


# handle the information revision logic
@login_required
def information_revise(request):
    username = request.session.get('name')
    user = UserAll.objects.get(name=username)
    if request.method == 'GET':
        init = {'email': user.email}  # used for initialize the form
        if user.identity == 's':
            init['address'] = user.seller.address
            init['fund'] = user.seller.fund
            init['phone'] = user.seller.phone
            revise_form = SellerInformationForm(initial=init)
        else:
            init['fund'] = user.customer.fund
            revise_form = CustomerInformationForm(initial=init)
        return render(request, 'usage/information-revise.html',{'form':revise_form})
    if request.method == 'POST':
        if user.identity == 's':
            revise_form = SellerInformationForm(request.POST, request.FILES)
            if revise_form.is_valid():
                address = revise_form.cleaned_data['address']
                phone = revise_form.cleaned_data['phone']
                avatar = revise_form.cleaned_data['avatar']
                user = UserAll.objects.get(name=username)
                user.avatar = avatar
                user.save()
                Seller.objects.filter(person=user).update(address=address, phone=phone)
                return redirect(reverse('usage:information_view'))
            else:
                return render(request, 'usage/information-revise.html',{'form':revise_form})
        if user.identity == 'c':
            revise_form = CustomerInformationForm(request.POST, request.FILES)
            if revise_form.is_valid():
                avatar = revise_form.cleaned_data['avatar']
                user.avatar =avatar
                user.save()
                return redirect(reverse('usage:information_view'))
            else:
                return render(request, 'usage/information-revise.html', {'form': revise_form})


@login_required
def my_order(request):
    username = request.session.get('name')
    try:
        seller = Seller.objects.get(person__name=username)
    except Seller.DoesNotExist:
        return render(request, 'forbidden.html')
    else:
        if request.method == 'GET':
            myOrder = Order.objects.filter(receiver=seller, status=False)
            return render(request, 'usage/order_handle.html', {'order': myOrder})
        if request.method == 'POST':
            try:
                for i in request.POST.getlist('order_list'):  # use the getlist not get
                    order = Order.objects.get(id=i)
                    order.status=True
                    seller.fund += order.good.price * order.number
                    order.save()
                seller.save()
            except TypeError:
                return redirect(reverse('usage:my_order'))
            else:
                return HttpResponse("修改成功")


def avatar_upload(request):
    username = request.session.get('name')
    user = UserAll.objects.filter(name=username)
    if request.method == 'GET':
        return render(request, 'usage/imagecrop.html')
    if request.method == 'POST':
        img = request.FILES
        user.update(avatar=img)
        return redirect(reverse('usage:information_view'))


# instantly return the photo to the page
@csrf_exempt
def report_upload(request):
    try:
        file = request.FILES['image']
        img = Image.open(file)           # use pillow to handle the pic
        print(1)
        try:
            # generate an unique code with file-text as a name for this pic, but slightly long
            file_name = str(uuid.uuid1()).replace("-", "") + os.path.splitext(file.name)[1]
            print(file_name+"upload")
            # save this pic in local server
            img.save(os.path.join(settings.MEDIA_ROOT, "image", file_name), img.format)
            return HttpResponse(settings.MEDIA_URL + 'image/{0}'.format(file_name))
        except Exception:
            return HttpResponse("error!!")  # can't save
    except Exception:
        return HttpResponse("error!")  # can't open

    
@login_required    
def order_history(request):
    username = request.session.get('name')
    user = UserAll.objects.get(name=username)
    if user.identity == 'c':
        return render(request, 'forbidden.html')
    if request.method == 'GET':
        orders = Order.objects.filter(receiver=user.seller)
        list_order,current_page = page_division(request, orders)
        return render(request, 'usage/order-history.html',{'orders':list_order, 'page':current_page})