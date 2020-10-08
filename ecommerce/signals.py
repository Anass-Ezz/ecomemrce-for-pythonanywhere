from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Profile, ShippingAddress


def user_profile(sender, instance, **kwargs):
    if Profile.objects.filter(user=instance).exists() == False:
        Profile.objects.create(user=instance,
                               email=instance.email,
                               first_name=instance.first_name,
                               last_name=instance.last_name)


post_save.connect(user_profile, sender=User)


def user_sipping_address(sender, instance, **kwargs):
    if ShippingAddress.objects.filter(user=instance).exists() == False:
        ShippingAddress.objects.create(user=instance)


post_save.connect(user_sipping_address, sender=User)
