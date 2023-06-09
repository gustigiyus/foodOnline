from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .context_processors import get_cart_amount, get_cart_counter
from .models import Cart
from menu.models import Category, FoodItem
from vendor.models import Vendor
from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.db.models import Q

from django.contrib.gis.measure import D # ``D`` is a shortcut for ``Distance``
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models.functions import Distance

# Create your views here.
def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_count': vendor_count,
    }
    return render(request, 'marketplace/listings.html', context)


def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)

    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset = FoodItem.objects.filter(is_available=True)
        )
    )

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None

    context = {
        'vendor': vendor,
        'categories': categories,
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/vendor_detail.html', context)


def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        # Check if using ajax request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Check if the food item exist
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # Check if user has already added that food to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    # Increase cart quantity
                    chkCart.quantity += 1
                    chkCart.save()
                    return JsonResponse({"status": "Success", "message": "Increase the cart quantity", "cart_counter": get_cart_counter(request), "qty": chkCart.quantity, "get_cart_amount": get_cart_amount(request)})
                except:
                    chkCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({"status": "Success", "message": "Added the product to the cart", "cart_counter": get_cart_counter(request), "qty": chkCart.quantity, "get_cart_amount": get_cart_amount(request)})
            except:
                return JsonResponse({"status": "Failed", "message": "This food does not exist"})
        else:
            return JsonResponse({"status": "Failed", "message": "Invalid request!"})
    else:
        return JsonResponse({"status": "login_required", "message": "Please login to continue"})
    

def decrease_cart(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Check if the food item exist
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # Check if user has already added that food to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    if chkCart.quantity > 1:
                        # Decrease the cart quantity
                        chkCart.quantity -= 1
                        chkCart.save()
                    else:
                        chkCart.delete()
                        chkCart.quantity = 0
                    return JsonResponse({"status": "Success", "message": "Decrease the cart quantity", "cart_counter": get_cart_counter(request), "qty": chkCart.quantity, "get_cart_amount": get_cart_amount(request)})
                except:
                    return JsonResponse({"status": "Failed", "message": "You don't have this item in your cart!"})
            except:
                return JsonResponse({"status": "Failed", "message": "This food does not exist"})
        else:
            return JsonResponse({"status": "Failed", "message": "Invalid request!"})
    else:
        return JsonResponse({"status": "login_required", "message": "Please login to continue"})
    

@login_required(login_url = 'login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    context = {
        'cart_items': cart_items,
        'get_cart_amount': get_cart_amount(request),
    }
    return render(request, 'marketplace/cart.html', context)


def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                # Check if the cart item is exist
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({"status": "Success", "message": "Cart item has been deleted!", "cart_counter": get_cart_counter(request), "get_cart_amount": get_cart_amount(request)})
            except:
                return JsonResponse({"status": "Failed", "message": "This item does not exist!"})      
        else:
            return JsonResponse({"status": "Failed", "message": "Invalid request!"})
        

def search(request):
    if not 'address' in request.GET:
        return redirect('marketplace')
    else :
        keyword = request.GET['keyword']
        address = request.GET['address']
        lat = request.GET['lat']
        lng = request.GET['lng']
        radius = request.GET['radius']

        # FINDING FOOD ITEM IN ALL VENODRS
        fetch_vendors_by_fooditems = FoodItem.objects.filter(food_title__icontains=keyword, is_available=True).values_list('vendor', flat=True)

        # FINDING VENDORS TAHT'S HAVE FOOD ITEM INIT 
        vendors = Vendor.objects.filter(Q(id__in=fetch_vendors_by_fooditems) | Q(vendor_name__icontains=keyword, is_approved=True, user__is_active=True))
        
        if lat and lng and radius:
            pnt = GEOSGeometry("POINT(%s %s)" % (lng, lat), srid=4326)
        
            # CEHCKING DISTANCE RESTAURANT
            vendors = Vendor.objects.filter(Q(id__in=fetch_vendors_by_fooditems) | Q(vendor_name__icontains=keyword, is_approved=True, user__is_active=True), 
            user_profile__location__distance_lte=(pnt, D(km=radius))
            ).annotate(distance=Distance("user_profile__location", pnt)).order_by("distance")

            for v in vendors:
                v.kms = round(v.distance.km, 1)
    
        # DEBUG QUERY
        # print(connection.queries)
        vendor_count = vendors.count()
        context = {
            'vendors': vendors,
            'vendor_count': vendor_count,
            'source_location': address.capitalize()
        }

    return render(request, 'marketplace/listings.html', context)
        
            

