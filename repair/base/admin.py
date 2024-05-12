from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import *
from .models import *
# Register your models here.

class CustomUserAdmin(UserAdmin):


    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ['email','id', 'first_name', 'last_name', 'is_staff']
    fieldsets = (
    (None, 
         {'fields':('email','phonenumber' ,'password',)}
     ),
    ('User Information',
        {'fields':('first_name', 'last_name')}
    ),
    ('Permissions', 
        {'fields':( 'is_staff', 'is_superuser', 'is_active', 'groups','user_permissions')}
    ),
    ('Registration', 
        {'fields':('date_joined', 'last_login',)}
    )
    )
    add_fieldsets = (
        (None, {'classes':('wide',),
            'fields':(
                'email', 'password1', 'password2',
            )}
            ),
        )
    search_fields = ("email",)
    ordering = ("email",)

admin.site.register(CustomUser, CustomUserAdmin)


class HandyManAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']
admin.site.register(HandyManCategory)
admin.site.register(HandyMan, HandyManAdmin)
admin.site.register(Client)
admin.site.register(Ad)
admin.site.register(Review)
# admin.site.register(CustomUser)
admin.site.register(Service)
admin.site.register(CartService)
admin.site.register(Cart)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id']
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderService)