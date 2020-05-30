from django.conf.urls import url
# from user import views
from user.views import RegisterView, ActiveView, LoginView, UserInfoView, UserOrderView, UserSiteView, LogOutView
# from django.contrib.auth.decorators import login_required

app_name = 'user'
urlpatterns = [
    # url(r"^register$", views.register, name='register'),
    url(r"^register$", RegisterView.as_view(), name='register'),
    url(r"^active/(?P<token>.+)$", ActiveView.as_view(), name='active'),
    url(r"^login$", LoginView.as_view(), name='login'),
    url(r"^logout$", LogOutView.as_view(), name='logout'),

    # url(r"^$", login_required(UserInfoView.as_view()), name='user'),
    # url(r"^order$", login_required(UserOrderView.as_view()), name='order'),
    # url(r"^site$", login_required(UserSiteView.as_view()), name='site'),

    url(r"^$", UserInfoView.as_view(), name='user'),
    url(r"^order/(?P<page>\d+)$", UserOrderView.as_view(), name='order'),
    url(r"^site$", UserSiteView.as_view(), name='site'),
]
