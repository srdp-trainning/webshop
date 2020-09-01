from django.contrib import admin
from usage.models import *

@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    list_per_page = 5
    list_display = ('id', 'date','writer_name')
    list_filter = ('writer__name', 'good__name')
    date_hierarchy = 'date'
    search_fields = ('date', 'writer__name', 'good__name')

    fields = ('body','id','date',)
    readonly_fields = ('id','date')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_per_page = 5
    list_display = ('id', 'date','status', 'number','sender_name', 'receiver_name', 'good_name')
    list_filter = ('receiver__person__name', 'status', 'good__name')
    date_hierarchy = 'date'

    search_fields = ('good__name','sender_name')
    fields = ('status','id','date','number')
    readonly_fields = ('id', 'date','number')
