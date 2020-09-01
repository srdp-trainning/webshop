from django.contrib import admin
from shop.models import *
from django import forms


class NewGoodForm(forms.ModelForm):

    class Meta:
        model = NewestGoods
        fields = '__all__'


# self-defined a filter, searching through price
class NewestGoodPriceFilter(admin.SimpleListFilter):
    title = "价格"
    parameter_name = 'price'

    def lookups(self, request, model_admin):
        return (
            ('case1',u"价格小于100"),
            ('case2',u"价格大于100小于1000"),
            ('case3',u"价格大于1000"),
        )

    def queryset(self, request, queryset):
        if self.value() == 'case1':
            return queryset.filter(price__lt='100')
        if self.value() == 'case2':
            return queryset.filter(price__gte='100',price__lt='1000')
        if self.value() == 'case3':
            return queryset.filter(price__gte='1000')


@admin.register(NewestGoods)
class NewestGoodAdmin(admin.ModelAdmin):

    # make good put on shelves
    def put_on_shelves(self, request, queryset):
        row_updated = queryset.update(on_sale=True)
        message_bit = "%s个商品" % row_updated
        self.message_user(request, "%s上架" % message_bit,)

    # make good put off shelves
    def put_off_shelves(self, request, queryset):
        row_updated = queryset.update(on_sale=False)
        message_bit = "%s个商品" % row_updated
        self.message_user(request, "%s下架" % message_bit)

    def delete_selected(self, request, queryset):
        flag = 1
        number = 0
        for i in queryset:
            good = Goods.objects.get(fake_id=i.fake_id)
            if good.order_good.all().filter(status=False):
                message_bit = "%s在订单里且未处理,不能删除" % i.name
                self.message_user(request, message_bit)
                flag = 0
                break
            else:
                number += 1
        if flag:
            for i in queryset:
                Goods.objects.filter(fake_id=i.fake_id).delete()
            queryset.delete()
            message_bit = "%s个商品删除" % number
            self.message_user(request, message_bit)

    delete_selected.short_description = "删除商品"
    put_off_shelves.short_description = "下架商品"
    put_on_shelves.short_description = "上架商品"

    list_filter = (
        (NewestGoodPriceFilter),
        ('owner', admin.RelatedOnlyFieldListFilter),
        ('on_sale', admin.BooleanFieldListFilter),
    )
    list_per_page = 4
    list_display = ('name', 'tags', 'price', 'stock',
                    'on_sale', 'owner_name')

    search_fields = ('tags', 'name', 'owner__person_name')
    fields = ('name','tags','price','stock','detail_information','on_sale', 'owner')

    actions = (put_off_shelves, put_on_shelves, delete_selected)
    form = NewGoodForm


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):

    def delete_cart(self, request, queryset):
        row_updated = 0
        for i in queryset:
            i.delte()
            row_updated += 1
        message_bit = "删除了%s个" % row_updated
        self.message_user(request, message_bit)

    list_display = ('customer', 'good', 'number')
    list_per_page = 4
    list_filter = (
        ('customer', admin.RelatedOnlyFieldListFilter),
    )
    search_fields = ('good', 'customer')
    actions = (delete_cart,)
    

