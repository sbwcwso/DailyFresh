from django.conf.urls import url
from cart import views


app_name = 'cart'
urlpatterns = [
    url("^add_cart$", views.AddCartView.as_view(), name="add_cart"),
    url("^$", views.ShowCartView.as_view(), name="show_cart"),
    url("^update_cart$", views.UpdateCartView.as_view(), name="update_cart"),
    url("^delete_cart$", views.DeleteCartView.as_view(), name="delete_cart"),
]
