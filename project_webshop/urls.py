from account.views import code_img
from django.conf.urls import url,include
from django.contrib import admin
from shop.views import home
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    url(r'^$',home, name='home'),
    url(r'^code/',code_img),
    url(r'^admin/', admin.site.urls),
    url(r'^home/',include(('account.urls', "account"),namespace='account')),
    # url(r'^tinymce/', include('tinymce.urls')),
    url(r'^shop/', include(('shop.urls', "shop"), namespace='shop')),
    url(r'^my/', include(('usage.urls',"usage"), namespace='usage')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
