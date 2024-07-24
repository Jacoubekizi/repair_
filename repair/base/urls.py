from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import *

urlpatterns = [
    path('auth/sign-up/', SignUp.as_view(), name='sign'),
    path('auth/sign-up-client/', SignUpClient.as_view(), name='sign-up-client'),
    path('auth/login/' , LoginUser.as_view() , name="login"),
    path('auth/logout/', LogoutUser.as_view(), name='logout'),
    path('auth/send-code/' , SendCodePassword.as_view() , name="send-code"),
    path('auth/verify-code/<str:pk>/' , VerifyCode.as_view() , name="verify-code"),
    path('auth/reset-password/<str:user_id>/' , ResetPassword.as_view(), name='reset-password'),
    path('auth/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('update-image/', UpdateImagteView.as_view(), name='update-image'),
    path('get-info-user/', RetrieveUserInfo.as_view(), name='get-info-user'),
    path('update-info-user/', UpdateUserInfo.as_view(), name='get-info-user'),

    path('cities/', CityHandymanCount.as_view(), name='cities'),
    path('categories/' , ListCategories.as_view() , name="list-categories"),
    path('list-ads/' , ListAds.as_view() , name="list-ads"),
    path('get-ad/<str:pk>/' , GetAd.as_view() , name="get-ads"),

    path('list-create-services/', ListCreateServices.as_view(), name='list-services'),
    path('get-service/<str:pk>/', GetService.as_view(), name='get-service'),

    path('create-handyman/', CreateHadnyMan.as_view(), name='create-handyman'),
    path('assign-category/<str:pk>/', AssignCategory.as_view(), name='assign-category'),
    path('list-handymen/', ListHandyMen.as_view(), name='list-handymen'),
    path('get-handymen/<str:pk>/', GetHandyMan.as_view(), name='get-handymen'),
    path('assign-service/<str:pk>/', AssignService.as_view(), name='assign-service'),
    path('get-info-handyman/', GetInfoHandyman.as_view(), name='get-info-handyman'),

    path('handyman-for-category/<str:category_id>/', HandymanForCategory.as_view(), name='handyman-for-category'),

    path('cart-handler/<str:service_id>/<str:action>/', CartServiceHandler.as_view(), name='cart-handler'),
    path('add-to-cart/<str:service_id>/' , AddServiceToCart.as_view() , name="add-to-cart"),
    path('create-cart-service/' , CreateCartService.as_view() , name="create-cart-service"),
    path('list-cart-services/' , ListCartServices.as_view() , name="list-cart-services"),

    path('create-order/<str:handy_man_id>/' , CreateOrder.as_view() , name="create-order"),
    path('set-date-time/' , SetDateTimeCart.as_view() , name="set-date-time"),
    path('orders/' , ListOrders.as_view() , name="list-orders"),
    path('reset-cart/' , ResetCartView.as_view() , name="reset-cart"),
    path('accept-order/<str:order_id>/' , AcceptOrder.as_view() , name="accept-order"),
    path('complete-order/<str:order_id>/' , CompleteOrder.as_view() , name="complete-order"),
    
    path('delete-order/<str:pk>/' , DeleteOrder.as_view() , name="delete-order"),
    path('create-reviews/<str:handy_man_id>/', CreateReviewsView.as_view(), name='create-reviews'),
    path('list-reviews/' , ListReviews.as_view() , name="list-reviews"),
    path('get-review/<str:pk>/' , GetReview.as_view() , name="get-review"),

]