from django.shortcuts import render, redirect
from .models import *
from django.views.generic import View, DetailView, CreateView, ListView, DeleteView
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, ShippingAddressForm
from allauth.account.forms import LoginForm
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.contrib import messages


class ProductList(ListView):
    model = Product
    template_name = "ecommerce/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product_list"] = Product.objects.filter(avalable=True)
        return context


class ProductDetail(DetailView):
    model = Product
    template_name = "ecommerce/detail.html"
    slug_url_kwarg = "slug"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        item = Product.objects.get(slug=self.kwargs["slug"])
        item.views += 1
        item.save()
        context = super().get_context_data(**kwargs)
        context["images"] = ProductImage.objects.filter(
            product__slug=self.kwargs["slug"]
        )
        context["bigvarients"] = VarientName.objects.filter(
            product__slug=self.kwargs["slug"]
        )
        return context


# this function handdle the functionality of
# >> adding items to cart
# >> and keeping the same product at the cart when the the varients are the same
#                           >> if the text is the same
#                           >> if the varient are the same
@login_required(login_url="/accounts/login/")
def add_item(request):
    if request.method == "POST":
        print(request)
        item = get_object_or_404(Product, slug=request.POST["slug"])
        order, create = Order.objects.get_or_create(
            user=request.user, ordered=False)
        varients_str = ""
        for var in request.POST:
            if "varient" in var:
                varients_str += request.POST[var] + "\n"
        order_item, create = OrderItem.objects.get_or_create(
            user=request.user,
            product=item,
            order=order,
            text=request.POST["text"],
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

    return redirect("ecommerce:product_detail", slug=request.POST["slug"])


def search(request):
    items = Product.objects.all()
    query = []
    for item in items:
        if request.GET["search"] in item.name or request.GET["search"] in item.desc:
            query.append(item)
        else:
            tags = item.tags.all()
            for tag in tags:
                if request.GET["search"] in str(tag):
                    query.append(item)
    context = {"product_list": query}
    return render(request, "ecommerce/list.html", context)


@login_required(login_url="/accounts/login/")
def cart_summery(request):
    try:
        order = Order.objects.get(user=request.user, ordered=False)
        cart_items = OrderItem.objects.filter(order=order, quantity__gte=1).order_by(
            "-order_date"
        )

        if cart_items.exists():
            total = 0
            for item in cart_items:
                total += item.item_total()
            order.order_total = round(total, 3)
            order.save()
            context = {"cart_items": cart_items, "order": order}
        else:
            context = {}

    except Order.DoesNotExist:
        context = {}
    return render(request, "ecommerce/cart.html", context)


@login_required(login_url="/accounts/login/")
def delete_item_from_cart(request):
    item = OrderItem.objects.get(user=request.user, id=request.GET["id"])
    item.delete()
    return redirect("ecommerce:cart_summery")


@login_required(login_url="/accounts/login/")
def manage_quantity(request):
    item = get_object_or_404(
        OrderItem, user=request.user, id=request.GET["id"])
    if request.GET["f"] == "-":
        item.quantity -= 1
        item.save()
        if item.quantity < 1:
            item.delete()
    else:
        if item.quantity < 10:
            item.quantity += 1
            item.save()
    return redirect("ecommerce:cart_summery")


def category(request):
    category = get_object_or_404(Category, id=request.GET["id"])
    products = Product.objects.filter(category=category)
    context = {"product_list": products}
    return render(request, "ecommerce/list.html", context)


@login_required(login_url="/accounts/login/")
def profile(request):
    if request.method == "POST":
        profile = Profile.objects.get(user=request.user)
        form = ProfileForm(request.POST, instance=profile)
        user = request.user
        user.first_name = request.POST["first_name"]
        user.last_name = request.POST["last_name"]
        user.save()
        if form.is_valid():
            profile_form = form.save(commit=False)
            profile_form.email = user.email
            form.save()

        return redirect("ecommerce:profile")
    else:
        profile = Profile.objects.get(user=request.user)
        form = ProfileForm(instance=profile)
        context = {"form": form, "profile": profile, "login_form": LoginForm}
        return render(request, "account/profile.html", context)


@login_required(login_url="/accounts/login/")
def edit_profile_photo(request):
    if request.method == "POST":
        profile = Profile.objects.get(user=request.user)
        photo = request.FILES["photo"]
        profile.photo = photo
        profile.save()
    return redirect("ecommerce:profile")


class SippingAddressView(View):
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            shipping_address = ShippingAddress.objects.get(
                user=self.request.user)
            form = ShippingAddressForm(instance=shipping_address)
            order = Order.objects.get(user=request.user, ordered=False)
            cart_items = OrderItem.objects.filter(
                order=order, quantity__gte=1
            ).order_by("-order_date")
            if cart_items.exists():
                total = 0
                for item in cart_items:
                    total += item.item_total()
            context = {"form": form, "cart_items": cart_items, "order": order}
            return render(request, "ecommerce/shipping_address.html", context)
        else:
            return redirect("/accounts/login/")

    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            order = Order.objects.get(user=request.user, ordered=False)
            shipping_address = ShippingAddress.objects.get(
                user=self.request.user)
            form = ShippingAddressForm(
                request.POST or None, instance=shipping_address)
            shipping_address.order = order
            shipping_address.save()
            if form.is_valid():
                try:
                    form.save()
                    order.ordered = True
                    order.order_date = timezone.now()
                    order.save()
                except:
                    pass
            return render(request, "ecommerce/order_saved.html")
        else:
            return redirect("/accounts/login/")


def my_orders(request):
    orders = Order.objects.filter(user=request.user, ordered=True).order_by(
        "-order_date"
    )
    context = {"orders": orders}
    return render(request, "ecommerce/my_orders.html", context)


def promo_code(request):
    if request.method == "POST":
        try:
            promo_code = PromoCode.objects.get(code=request.POST["code"])
        except PromoCode.DoesNotExist:
            promo_code = None
        if promo_code:
            order = Order.objects.get(user=request.user, ordered=False)
            if order.promo_code:
                messages.add_message(
                    request, messages.WARNING, "promo code already taken"
                )
            else:
                order.promo_code = promo_code.code
                order.discount = promo_code.percent
                order.save()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    f"congratulations you saved {promo_code.percent} %",
                )
        else:
            messages.add_message(request, messages.WARNING,
                                 "promo code not found")
    return redirect("/cart")
