from rest_framework import serializers
from ecommerce.models import *
from django_countries.serializer_fields import CountryField


class VarientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Varient
        fields = "__all__"


class VarientNameSerializer(serializers.ModelSerializer):
    varient = VarientSerializer(many=True)

    class Meta:
        model = VarientName
        fields = "__all__"


class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    product_images = ProductImagesSerializer(many=True,  read_only=True)
    varient_names = VarientNameSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False, read_only=True)
    total = serializers.CharField(source='item_total', read_only=True)

    class Meta:
        model = OrderItem
        fields = "__all__"


class ActiveOrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'
