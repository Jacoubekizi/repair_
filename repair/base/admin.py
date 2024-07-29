from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import *
from .models import *
# Register your models here.


admin.site.site_header = "Repair administration"
admin.site.index_title = "Repair administration"

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
    list_display = ['id', 'user', 'name', 'city']
    search_fields = ['name', 'city', 'user__phonenumber']

    fieldsets = (
        ('Handyman Information',
        
            {'classes':('wide',), 'fields':('name', 'city', 'user__phonenumber')}
        ),
        ('Classification',
            {'classes':('wide',),
            'fields':('category','services')},

        ),
    )
admin.site.register(HandyMan, HandyManAdmin)

class HandyManCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created']
    search_fields = ['name']

    fieldsets = (
        ('Category Information',
            {
                'classes':('wide',), 
                'fields':('name', 'image')
            }
        ),
    )
admin.site.register(HandyManCategory, HandyManCategoryAdmin)

class ClientAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'phonenumber']

    def name(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'
    
    def phonenumber(self, obj):
        return obj.user.phonenumber.as_international
    
    def email(self, obj):
        return obj.user.email
admin.site.register(Client, ClientAdmin)

class AdAdmin(admin.ModelAdmin):
    list_display = ['id', 'description']

    fieldsets = (
        ('Ad Information',
            {
                'classes':('wide',), 
                'fields':('description', 'image')
            }
        ),
    )
admin.site.register(Ad, AdAdmin)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'handyman', 'rating']

    fieldsets = (
        ('Review Details',
            {
                'classes':('wide',), 
                'fields':('user', 'handyman', 'rating')
            }
        ),
    )

    def name_user(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'
    
    def handyman_name(self, obj):
        return obj.handyman.name
admin.site.register(Review, ReviewAdmin)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'cost']
    search_fields = ['name']

    fieldsets = (
        ('Service Details',
            {
                'classes':('wide',), 
                'fields':('name', 'image', 'cost')
            }
        ),
    )
admin.site.register(Service, ServiceAdmin)

class CartServiceAdmin(admin.ModelAdmin):
    list_display = ['service', 'quantity', 'cost']
    search_fields = ['service']

    fieldsets = (
        ('Cart Service Details',
            {
                'classes':('wide',), 
                'fields':('name', 'quantity', 'cost')
            }
        ),
    )
admin.site.register(CartService, CartServiceAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'time']

    def user(self, obj):
        return f'{obj.client.user.first_name} {obj.client.user.last_name}'
    
    fieldsets = (
        ('Cart Details',
            {
                'classes':('wide',), 
                'fields':('client', 'service', 'date', 'time')
            }
        ),
    )   
admin.site.register(Cart, CartAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'handyman', 'client', 'accepted', 'completed']
    list_filter = ['accepted', 'completed']
    search_fields = ['hand_yman__name', 'client__user__phonenumber']

    def handyman(self, obj):
        return obj.handy_man.name
    
    def client(self, obj):
        return f'{obj.client.user.first_name} {obj.client.user.last_name}'

    fieldsets = (
        ('Order Details',
            {
                'classes':('wide',), 
                'fields':('handy_man', 'client', 'service', 'accepted', 'completed', 'date', 'time')
            }
        ),
    )
admin.site.register(Order, OrderAdmin)

class OrderServiceAdmin(admin.ModelAdmin):
    list_display = ['service', 'quantity', 'cost']
    search_fields = ['service']

    fieldsets = (
        ('Order Service Details',
            {
                'classes':('wide',), 
                'fields':('service', 'quantity', 'cost')
            }
        ),
    )
admin.site.register(OrderService, OrderServiceAdmin)