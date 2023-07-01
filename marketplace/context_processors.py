from .models import Cart
from menu.models import FoodItem


def get_cart_counter(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart_item = Cart.objects.filter(user=request.user)
            if cart_item:
                for cart_item in cart_item:
                    cart_count += cart_item.quantity
            else:
                cart_count = 0
        except:
            cart_count = 0
    return dict(cart_count=cart_count)


def get_cart_amount(request):
    subtotal = 0
    tax = 0
    grand_total = 0
    if request.user.is_authenticated:
        try: 
            cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
            if cart_items:
                for cart_item in cart_items:
                    ttl = cart_item.quantity * cart_item.fooditem.price
                    subtotal += ttl
                    tax = ((subtotal / 100) * 4)
                    grand_total = (((subtotal / 100) * 4) + subtotal)
        except:
            subtotal = 0
            tax = 0
            grand_total = 0
    return dict(subtotal=subtotal, tax=tax, grand_total=grand_total)
