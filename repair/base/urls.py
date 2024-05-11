from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import *

urlpatterns = [
    path('auth/sigin/', SignUpView.as_view(), name='sigin'),
    # path('auth/verify-account/<str:pk>/', VerifyAccount.as_view(), name='verify-account'),
    path('auth/login/' , LoginUser.as_view() , name="login"),
    path('auth/logout/', LogoutUser.as_view(), name='logout'),
    path('auth/send-code/' , SendCodePassword.as_view() , name="send-code"),
    path('auth/verify-code/<str:pk>/' , VerifyCode.as_view() , name="verify-code"),
    path('auth/reset-password/<str:user_id>/' , ResetPassword.as_view(), name='reset-password'),
    path('auth/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('update-image/', UpdateImagteView.as_view(), name='update-image'),
    # path('update-email/', UpdateEmailView.as_view(), name='update-email'),
    path('get-info-user/', RetrieveInfoUser.as_view(), name='get-info-user'),
    path('cities/', CityHandymanCount.as_view(), name='cities'),
    path('cart-handler/<str:service_id>/<str:action>/', CartServiceHandler.as_view(), name='cart-handler'),
    path('add-to-cart/<str:service_id>/' , AddServiceToCart.as_view() , name="add-to-cart"),
    path('create-cart-service/' , CreateCartService.as_view() , name="create-cart-service"),
    path('list-cart-services/<str:cart_id>/' , ListCartServices.as_view() , name="list-cart-services"),
    path('list-handymen/', ListHandyMen.as_view(), name='list-handymen'),
    path('get-handymen/<str:pk>/', GetHandyMan.as_view(), name='get-handymen'),
    path('orders/' , ListOrders.as_view() , name="list-orders"),
    path('categories/' , ListCategories.as_view() , name="list-categories"),
    path('accept-order/<str:pk>/' , AcceptOrder.as_view() , name="accept-order"),
    path('complete-order/<str:pk>/' , CompleteOrder.as_view() , name="complete-order"),
    path('list-ads/' , ListAds.as_view() , name="list-ads"),
    path('delete-order/<str:pk>/' , DeleteOrder.as_view() , name="delete-order"),
    path('create-handman/', CreateHadnyMan.as_view(), name='create-handyman')
]
