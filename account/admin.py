from django.contrib import admin
from account.models import *
from shop.models import NewestGoods, ShoppingCart
from django.utils.safestring import mark_safe

admin.site.disable_action('delete_selected')


class GoodDisplay(admin.TabularInline):
    model = NewestGoods
    fields = ('name','tags','price','stock', 'id', 'on_sale'),
    readonly_fields = ('id',)
    extra = 3


class ShoppingCartDisplay(admin.TabularInline):
    model = ShoppingCart
    fields = ('good','number'),
    extra = 3
    raw_id_fields = ('good',)


@admin.register(UserAll)
class UserAllAdmin(admin.ModelAdmin):
    fields = ('name', 'email', 'avatar', 'img', 'identity')
    list_display = ('id', 'name', 'email', 'img', 'identity')
    readonly_fields = ('img','name','identity')
    list_per_page = 5
    list_filter = ('identity',)
    search_fields = ('name',)
    list_editable = ('email',)
    ordering = ('name',)
    actions = ('delete_selected',)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    search_fields = ('person',)
    fieldsets = (
        ('用户信息', {
            'fields':('person',)
        }),
        ('收藏',{
            'classes': ('collapse',),
            'fields':('fund',),
        }),

        )
    list_display = ('person', 'fund')
    readonly_fields = ('person', 'fund')
    list_per_page = 5
    inlines = [ShoppingCartDisplay]
    

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):

    # cancel the qualification of seller for selling goods
    def cancel_seller(self, request, queryset):
        row_updated = queryset.update(store_status=False)
        message_bit = "注销了%s个商家的销售权" % row_updated
        self.message_user(request, message_bit)
    cancel_seller.short_description = "注销商家销售权"

    def restore_seller(self, request, queryset):
        row_updated = queryset.update(store_status=True)
        message_bit = "恢复了%s个商家的销售权" % row_updated
        self.message_user(request, message_bit)
    restore_seller.short_description = "恢复商家销售权"

    def view_phone(self, obj):
        return obj.phone
    view_phone.empty_value_display = '???'

    def view_address(self, obj):
        return obj.address
    view_address.empty_value_display = '???'


    search_fields = ('person',)
    fields = ('person', 'fund', 'phone', 'address', 'store_status')
    readonly_fields = ('person', 'fund',)

    list_display = ('person', 'view_phone','fund', 'view_address', 'store_status',)
    list_per_page = 5

    inlines = [GoodDisplay]
    actions = (cancel_seller, restore_seller)



