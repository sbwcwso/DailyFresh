from django.conf.urls import url

from user.views import (
    RegisterView, ActiveView, LoginView,
    UserInfoView, UserOrderView, UserSiteView,
    LogOutView,
)

app_name = 'user'
urlpatterns = [
    # 用户注册，激活，登入，登出
    url(r"^register$", RegisterView.as_view(), name='register'),
    url(r"^active/(?P<token>.+)$", ActiveView.as_view(), name='active'),
    url(r"^login$", LoginView.as_view(), name='login'),
    url(r"^logout$", LogOutView.as_view(), name='logout'),

    # 用户信息页面，订单页面，收货地址等
    url(r"^$", UserInfoView.as_view(), name='user'),
    url(r"^order/(?P<page>\d+)$", UserOrderView.as_view(), name='order'),
    url(r"^site$", UserSiteView.as_view(), name='site'),
]
