from django.conf.urls import url,include
from usage import views


urlpatterns = [
    url(r'^new/', views.new_good, name='new',),
    url(r'^list/', views.my_store, name='list'),
    url(r'^detail/(?P<fake_id>.*)$',views.my_good, name='detail'),
    url(r'^revise/(?P<fake_id>.*)$', views.good_revise, name='revise'),
    url(r'^information-view/',views.information_view, name='information_view'),
    url(r'^information-revise/', views.information_revise, name='information_revise'),
    url(r'^my-order/', views.my_order, name='my_order'),
    url(r'^upload-avatar', views.avatar_upload, name='avatar_upload'),
    url(r'^upload-photo/', views.report_upload, name='upload_img'),
    url(r'^order-history', views.order_history, name='order_history'),
]