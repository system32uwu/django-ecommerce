from django.urls import path
from django.conf.urls import include, url

from . import views

urlpatterns = [
    path("", views.store, name="store"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("update_item/", views.updateItem, name="update_item"),
    path("process_order/", views.processOrder, name="process_order"),
    path("confirm_payment/", views.confirmPayment, name="confirm_payment"),
    path("login/", views._login, name="login"),
    path("auth/", views._loginEndPoint, name="auth"),
    path("logout/", views._logout, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("upd_personal_info/", views.updPersonalInfo, name="updPersonalInfo"),
    path("register/", views.register, name="register"),
    path("save_user/", views._registerEndPoint, name="save_user"),
]