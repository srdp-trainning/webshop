from django.conf.urls import url
from account import views
urlpatterns = [
    url(r'^login/', views.login,name='login'),
    url(r'^register/', views.register, name='register'),
    url(r'^reset/', views.password_reset,name='reset'),
    url(r'^modify', views.password_change, name='modify')
]