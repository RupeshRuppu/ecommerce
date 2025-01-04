from django.urls import path

from . import views

# auth related urls
urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("refresh-token/", views.refresh_token, name="refresh-token"),
]

# product related upload urls
urlpatterns += [
    path("profile-upload/", views.profile_upload),
    path("product-upload/", views.product_upload),
]

# product related get urls
urlpatterns += [
    path("get-products/", views.get_products),
    path("get-product/<str:pid>", views.get_product),
    path("get-categories/", views.get_categories),
]
