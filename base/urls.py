from django.contrib import admin
from django.urls import path, include

from base.views import index

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="index"),
    path("", include("blog.urls")),
]
