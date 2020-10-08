from .models import *
from allauth.account.forms import LoginForm


def categories(request):
    return {
        'categories': Category.objects.all(),
    }


def user_short_name(request):
    user_short = request.user.username[:2].upper()
    return {'user_short': user_short}


def login_form(request):

    return {"login_form": LoginForm}


def items_len(request):
    try:
        order = Order.objects.get(user=request.user, ordered=False)
        items = OrderItem.objects.filter(order=order)
        num = len(items)
    except:
        num = 0
    return {'items_len': num}


def user_image(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        profile_image = profile.photo
        return {
            'profile_image': profile_image,
        }
    else:
        return {
            'profile_image': 'no',
        }
