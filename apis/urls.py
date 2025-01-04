from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("refresh-token/", views.refresh_token, name="refresh-token"),
]

urlpatterns += [
    path("profile-upload/", views.profile_upload),
    path("product-upload/", views.product_upload),
]
