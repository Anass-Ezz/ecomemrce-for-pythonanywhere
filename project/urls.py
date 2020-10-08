from django.contrib import admin
from django.urls import path, include
from ecommerce import urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("ecommerce.urls")),
    path("accounts/", include("allauth.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include("API.urls")),
    # path("api/accounts/", include("dj_rest_auth.urls")),
]
