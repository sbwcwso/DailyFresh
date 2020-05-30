from django.conf.urls import url
from order import views
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

app_name = 'order'
urlpatterns = [
    url("^place$", views.OrderPlaceView.as_view(), name="place"),
    url("^commit$", views.OrderCommitView.as_view(), name="commit"),
    url("^pay$", views.OrderPayView.as_view(), name="pay"),
    url("^check$", views.OrderCheckView.as_view(), name="check"),
    url("^notify$", csrf_exempt(views.OrderNotifyView.as_view()), name="notify"),
    url("^comment/(?P<order_id>\d+)$", views.OrderCommentView.as_view(), name="comment"),
]
