from django.conf.urls import include, url
from django.contrib import admin

from goods.views import NewSearchView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^tinymce/', include('tinymce.urls')),  # 富文本编辑器
    url(r'^search/', NewSearchView()),  # 全文检索框架
    url(r'^', include('goods.urls', namespace='goods')),
    url(r'^user/', include('user.urls', namespace='user')),
    url(r'^cart/', include('cart.urls', namespace='cart')),
    url(r'^order/', include('order.urls', namespace='order')),
]
