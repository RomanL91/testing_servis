from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include(("authapp.urls", "authapp"), namespace="authapp")),
    path("", include(("testapp.urls", "testapp"), namespace="testapp")),
]
