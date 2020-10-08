from django.conf.urls import url
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib import admin

admin.site.site_header = "MINE Admin"
admin.site.site_title = "MINE Admin Portal"
admin.site.index_title = "Welcome to MINE Researcher Portal"

app_name = "ecommerce"

urlpatterns = (
    [
        path("", views.ProductList.as_view(), name="product_list"),
        path("<slug:slug>/", views.ProductDetail.as_view(), name="product_detail"),
        path("addtocart", views.add_item, name="add_item"),
        path("my_orders", views.my_orders, name="my_orders"),
        path("promocode", views.promo_code, name="promo_code"),
        path("search", views.search, name="search"),
        path("cart", views.cart_summery, name="cart_summery"),
        path("profile", views.profile, name="profile"),
        path("quantity", views.manage_quantity, name="manage_quantity"),
        path("category", views.category, name="category"),
        path("delete", views.delete_item_from_cart, name="delete"),
        path("editprofilephoto", views.edit_profile_photo, name="edit_profile_photo"),
        path(
            "shipping_address",
            views.SippingAddressView.as_view(),
            name="setting_shipping_address",
        ),
        #    path("api/product/", api.product_list_api, name="product_list_api"),
        #    path(
        #        "api/product/<slug:slug>",
        #        api.product_details_api,
        #        name="product_details_api",
        #    ),
        #    path("api/addtocard/", api.add_to_card_api, name="add_to_card_api"),
        #    path("api/cart_items/", api.cart_items, name="cart_items"),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
