from django.conf.urls import url
from order import views
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

app_name = 'order'
urlpatterns = [
    url(r"^place$", views.OrderPlaceView.as_view(), name="place"),
    url(r"^commit$", views.OrderCommitView.as_view(), name="commit"),
    url(r"^pay$", views.OrderPayView.as_view(), name="pay"),
    url(r"^check$", views.OrderCheckView.as_view(), name="check"),
    url(r"^notify$", csrf_exempt(views.OrderNotifyView.as_view()), name="notify"),
    url(r"^comment/(?P<order_id>\d+)$", views.OrderCommentView.as_view(), name="comment"),
]
