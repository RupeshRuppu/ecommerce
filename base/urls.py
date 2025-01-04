from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path


def main(req):
    return render(req, "main.html")


urlpatterns = [
    path("", main),
    path("admin/", admin.site.urls),
]

# apis specific urls
urlpatterns += [path("apis/v1/", include("apis.urls"))]
