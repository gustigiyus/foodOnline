from django.contrib import admin
from .models import User, UserProfile
from django.contrib.auth.admin import UserAdmin

# Configure admin panel views.
class CustomUserAdmin(UserAdmin):
    list_display = ("email", "first_name", "last_name", "username", "role", "is_admin")
    ordering = ("-date_joined", )
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


# Register your models here to admin panels.
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)