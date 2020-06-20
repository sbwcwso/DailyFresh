from django.conf.urls import url
from goods import views

app_name = 'goods'

urlpatterns = [
    url(r"^index$", views.IndexView.as_view(), name="index"),
    url(r"^goods/(?P<goods_id>\d+)$", views.DetailView.as_view(), name="detail"),
    url(r"^list/(?P<type_id>\d+)/(?P<page>\d+)$", views.GoodsListView.as_view(), name="list"),
]
