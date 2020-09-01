from django.conf.urls import url
from shop import views

urlpatterns = [
    url(r'^good-display/', views.good_list, name='good_display'),
    url(r'^cart/', views.my_cart, name='cart'),
    url(r'^good-detail/(?P<fake_id>.*)/$', views.good_detail, name='good_detail'),
    url(r'^good-detail/(?P<fake_id>.*)/(?P<review_id>\d+)/reply$', views.reply, name= 'reply'),
    url(r'^deposit/', views.deposit, name='deposit'),
    url(r'^shopping_detail', views.shopping_detail, name='shopping_detail'),
    url(r'^order-detail/(?P<code>.*)$', views.order_detail, name='order-detail'),
    url(r'^purchase/(?P<fake_id>.*)$', views.good_purchase, name='good_purchase'),
    url(r'password-change', views.password_change, name='password_change'),
]