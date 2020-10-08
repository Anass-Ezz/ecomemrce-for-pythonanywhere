from django.urls import path, include
from .restAPI import api

app_name = "API"


urlpatterns = [
    path("accounts/", include("dj_rest_auth.urls")),
    path("product/", api.product_list_api, name="product_list_api"),
    path(
        "product/<slug:slug>",
        api.product_details_api,
        name="product_details_api",
    ),
    path("addtocard/", api.add_to_card_api, name="add_to_card_api"),
    path("active_order/", api.active_order, name="cart_items"),
    path('quantity/', api.manage_quantity, name="manage_quantity"),
    path('remove_item/', api.remove_item, name="remove_item"),
    path('search/', api.search, name="search"),
    path('promo_code/', api.promo_code, name="promo_code"),
    path('profile/', api.ProfileApi.as_view(), name="promo_code"),
]
