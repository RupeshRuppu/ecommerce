from django.urls import path
from .views import profile_upload, product_upload
from .views import *

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("refresh-token/", refresh_token, name="refresh-token"),
]

urlpatterns += [
    path("profile-upload/", profile_upload),
    path("product-upload/", product_upload),
]
