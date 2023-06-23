from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.marketplace, name="marketplace"),
    path('<slug:vendor_slug>/', views.vendor_detail, name='vendor_detail'),

    # ADD TO CART
    path('add_to_cart/<int:food_id>/', views.add_to_cart, name='add_to_cart'), 
    # DECREASE TO CART
    path('decrease_cart/<int:food_id>/', views.decrease_cart, name='decrease_cart'),   
]   