from django.contrib import admin
from .models import *
import admin_thumbnails
from django.forms import TextInput, Textarea

# Register your models here.

# for orders


class InLineOrderItems(admin.TabularInline):
    model = OrderItem
    readonly_fields = ("user", "related_product", "product", "quantity",
                       "text", "varients", 'ordered')
    list_display_links = ("product", "quantity")
    extra = 0
    formfield_overrides = {
        models.CharField: {
            'widget': TextInput(attrs={'size': '20'})
        },
        models.TextField: {
            'widget': Textarea(attrs={
                'rows': 4,
                'cols': 40
            })
        },
    }


class InLineShippingAddress(admin.TabularInline):
    model = ShippingAddress
    readonly_fields = ("user", "first_name", "last_name", "address_1",
                       "address_2", "country", "state", 'city', "zip_code",
                       'phone')
    list_display_links = ("user", "phone")
    extra = 0
    formfield_overrides = {
        models.CharField: {
            'widget': TextInput(attrs={'size': '20'})
        },
        models.TextField: {
            'widget': Textarea(attrs={
                'rows': 4,
                'cols': 40
            })
        },
    }


class OrderAdmin(admin.ModelAdmin):
    fields = (
        'user',
        'order_total',
        'ordered',
        'promo_code',
        'discount',
        'after_discount_total',
        'status',
        'progress',
        'amana_number',
    )
    radio_fields = {'progress': admin.HORIZONTAL}
    list_display = (
        "user",
        "id",
        "ordered",
        "order_date",
        "status",
    )
    list_filter = ("status", "ordered", "order_date")
    search_fields = ('id', )
    list_editable = ('status', )
    readonly_fields = (
        'user',
        'ordered',
        'promo_code',
        'discount',
        'after_discount_total',
        'order_total',
    )
    inlines = [InLineOrderItems, InLineShippingAddress]


# for products
class InLineProductImage(admin.TabularInline):
    model = ProductImage
    extra = 1


class InLineVarientName(admin.TabularInline):
    autocomplete_fields = ('varient', )
    model = VarientName
    extra = 0
    max_num = 6


@admin_thumbnails.thumbnail('image')
class ProductAdmin(admin.ModelAdmin):
    search_fields = ('id', 'pk')
    inlines = [InLineProductImage, InLineVarientName]
    list_display = ("name", "price", "category", 'image_thumbnail')
    formfield_overrides = {
        models.CharField: {
            'widget': TextInput(attrs={'size': '20'})
        },
        models.TextField: {
            'widget': Textarea(attrs={
                'rows': 4,
                'cols': 40
            })
        },
    }


# for varientName
class VarientNameAdmin(admin.ModelAdmin):
    autocomplete_fields = ('varient', )


class VarientAdmin(admin.ModelAdmin):
    search_fields = ('name', )


# for promo code
class PromoCodeAdmin(admin.ModelAdmin):
    search_fields = ('id', 'code')
    list_display = ('id', 'code', 'percent')


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(ProductImage)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Varient, VarientAdmin)
admin.site.register(VarientName, VarientNameAdmin)
admin.site.register(Profile)
admin.site.register(ShippingAddress)
admin.site.register(PromoCode, PromoCodeAdmin)
