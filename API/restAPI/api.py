from ecommerce.models import *
from .serializer import *
from django.http import HttpResponse, JsonResponse
from rest_framework import status, permissions, authentication
from django_countries import countries
from rest_framework.views import APIView
import time
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404

from ecommerce import views


@permission_classes([AllowAny])
def product_list_api(request):
    if request.method == "GET":
        products = Product.objects.all()
        serialized_products = ProductSerializer(products, many=True).data
        return JsonResponse(
            {
                "serialized_products": serialized_products,
            },
            safe=False,
        )


@permission_classes([AllowAny])
def product_details_api(request, slug):
    if request.method == "GET":
        product = Product.objects.get(slug=slug)

        serialized_product = ProductSerializer(product).data
        return JsonResponse(
            {
                "serialized_product": serialized_product,

            },
            safe=False,
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_to_card_api(request):
    data = request.data["text"]
    print(data)
    item = get_object_or_404(Product, slug=request.data["slug"])
    order, create = Order.objects.get_or_create(
        user=request.user, ordered=False)
    varients_str = ""
    for var in request.data:
        if "varient" in var:
            varients_str += request.data[var] + "\n"
    order_item, create = OrderItem.objects.get_or_create(
        user=request.user,
        product=item,
        order=order,
        text=request.data["text"],
        varients=varients_str,
    )
    # if the item is already in the cart encrease the quantity
    if not create:
        order_item.quantity += 1
        order_item.save()
    # saving the order total when adding each item to cart
    cart_items = OrderItem.objects.filter(order=order, quantity__gte=1)
    if cart_items.exists():
        total = 0
        for item in cart_items:
            total += item.item_total()
        order.order_total = round(total, 3)
        order.items.add(order_item)
        order.save()
    return Response("done", status=200)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def active_order(request):
    order = Order.objects.get(user=request.user, ordered=False)
    serialized_active_order = ActiveOrderSerializer(order).data
    return JsonResponse(serialized_active_order)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def manage_quantity(request):
    order = Order.objects.get(user=request.user, ordered=False)
    cart_items = OrderItem.objects.filter(user=request.user, order=order)
    item = OrderItem.objects.get(id=request.GET['id'])
    if int(request.GET['quantity']) in range(1, 11):
        item.quantity = request.GET['quantity']
        item.save()
    order.save()
    return Response('done')


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def remove_item(request):
    item = OrderItem.objects.get(id=request.GET['id'])
    item.delete()
    Order.objects.get(user=request.user, ordered=False).save()
    return Response('done')


@api_view(['GET'])
@permission_classes([AllowAny])
def search(request):
    items = Product.objects.all()
    query = []
    for item in items:
        if request.GET["search"] in item.name or request.GET["search"] in item.desc:
            if item not in query:
                query.append(item)
        else:
            tags = item.tags.all()
            for tag in tags:
                if request.GET["search"] in str(tag):
                    query.append(item)
    serialized_search = ProductSerializer(query, many=True).data
    return Response(serialized_search)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def promo_code(request):
    time.sleep(2)
    order = Order.objects.get(user=request.user, ordered=False)
    if not order.promo_code:
        try:
            promo_code = PromoCode.objects.get(code=request.GET['code'])
            order.promo_code = promo_code.code
            order.discount = promo_code.percent
            order.save()
            return Response('discount code added successfully', status=status.HTTP_200_OK)
        except PromoCode.DoesNotExist:
            return Response('discount code not found try aggain', status=status.HTTP_204_NO_CONTENT)

    else:
        return Response('dicount code is already tokefdfdn', status=status.HTTP_208_ALREADY_REPORTED)
    # return Response('done')


class ProfileApi(APIView):
    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        serialized_profile = ProfileSerializer(profile, many=False).data
        return Response({'serialized_profile': serialized_profile, 'countries': countries}, status=status.HTTP_200_OK)

    def post(self, request):
        time.sleep(1)
        profile = Profile.objects.get(user=request.user)
        data = request.data['data']
        profile.first_name = data['first_name']
        profile.last_name = data['last_name']
        profile.country = data['country']
        try:
            int(data['phone'])
            profile.phone = data['phone']
        except:
            pass
        profile.save()
        serialized_profile = ProfileSerializer(profile, many=False).data
        return Response(serialized_profile)
