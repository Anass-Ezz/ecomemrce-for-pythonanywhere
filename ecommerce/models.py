from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.utils.text import slugify
from django_countries.fields import CountryField
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

user = User.objects.all()

EXEPTION_CHOICES = [
    ("s", "sold"),
    ("n", "new"),
]


class Product(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField(max_length=1000, verbose_name="Discription")
    price = models.FloatField()
    avalable = models.BooleanField(default=True, blank=True)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images", null=True, blank=True)
    slug = models.SlugField(blank=True, null=True, unique=True)
    old_price = models.FloatField(null=True, blank=True)
    tags = TaggableManager()
    views = models.IntegerField(default=0)
    exeption = models.CharField(
        max_length=100, choices=EXEPTION_CHOICES, default="n")
    add_date = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def percent(self):
        percent = 100 - (self.price * 100) / self.old_price
        return int(percent)

    def get_absolute_url(self):
        return reverse("ecommerce:product_detail", kwargs={"slug": self.slug})


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(blank=True, max_length=14)
    photo = models.ImageField(
        upload_to="images", default="images/default_img.png")
    country = CountryField(blank=True)

    def __str__(self):
        return self.user.username


class ProductImage(models.Model):
    image = models.ImageField(upload_to="images")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, related_name='product_images')

    def __str__(self):
        return str(self.image)


class Category(models.Model):
    name = models.CharField(max_length=100)
    disc = models.TextField(max_length=1000)
    image = models.ImageField(upload_to="images", blank=True, null=True)

    def __str__(self):
        return str(self.name)


STATUS_CHOICES = [
    ("c", "consulting"),
    ("w", "working on"),
    ("s", "shipping"),
]
PROGRESS_CHOICES = [
    ("25", "25%"),
    ("50", "50%"),
    ("75", "75%"),
    ("100", "100%"),
]


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default="c")
    order_total = models.FloatField(
        max_length=10, blank=True, null=True, verbose_name="order total (mad)"
    )
    items = models.ManyToManyField('OrderItem', related_name="item")
    amana_number = models.CharField(max_length=100, null=True, blank=True)
    promo_code = models.CharField(max_length=50, null=True, blank=True)
    discount = models.FloatField(null=True, blank=True)
    after_discount_total = models.FloatField(null=True, blank=True)
    progress = models.CharField(
        choices=PROGRESS_CHOICES, max_length=10, default="25")

    def __str__(self):
        return str(self.user.username)

    def save(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.user, ordered=False)
            order_items = order.items.all()
            total = 0
            for item in order_items:
                total += item.item_total()
            self.order_total = total
        except:
            pass
        if self.discount:
            discount_amount = round(
                self.order_total * (self.discount / 100), 3
            )
            self.after_discount_total = round(
                self.order_total - discount_amount, 3)
        else:
            self.after_discount_total = self.order_total

        super(Order, self).save(*args, **kwargs)


class OrderItem(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True
    )
    quantity = models.PositiveSmallIntegerField(
        default=1, null=True, blank=True)
    ordered = models.BooleanField(default=False)
    order = models.ForeignKey(
        "Order", on_delete=models.CASCADE, related_name='order_items')
    order_date = models.DateTimeField(auto_now_add=True, null=True)
    text = models.CharField(max_length=12, null=True)
    varients = models.TextField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return str(self.product.name)

    def related_product(self):
        return self.product.id

    def item_total(self):
        return round(self.quantity * self.product.price, 2)


class VarientName(models.Model):
    name = models.CharField(max_length=100)
    varient = models.ManyToManyField(
        "Varient", blank=True, related_name="varient_names")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, related_name='varient_names')

    def __str__(self):
        return self.name


class PromoCode(models.Model):
    code = models.CharField(max_length=100, unique=True)
    disc = models.TextField(max_length=1000, verbose_name="Discription")
    percent = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(30)],
        verbose_name="discount percentage (%)",
    )

    def __str__(self):
        return self.code


class Varient(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to="images", blank=True)

    def __str__(self):
        return self.name


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(
        Order, null=True, blank=True, on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    address_1 = models.CharField(max_length=100, blank=True, null=True)
    address_2 = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    country = CountryField(default="Morocco", blank=True, null=True)
    zip_code = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.username
