from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import *

urlpatterns = [
    path('auth/sign-up/', SignUpView.as_view(), name='sign-up'),
    path('auth/sign-up-for-client/', SignUpViewForClient.as_view(), name='sign-up-for-client'),
    path('auth/login/' , LoginUser.as_view() , name="login"),
    path('auth/logout/', LogoutUser.as_view(), name='logout'),
    path('auth/send-code/' , SendCodePassword.as_view() , name="send-code"),
    path('auth/verify-code/<str:pk>/' , VerifyCode.as_view() , name="verify-code"),
    path('auth/reset-password/<str:user_id>/' , ResetPassword.as_view(), name='reset-password'),
    path('auth/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('update-image/', UpdateImagteView.as_view(), name='update-image'),
    path('get-info-user/', RetrieveInfoUser.as_view(), name='get-info-user'),
    path('update-info-user/', UpdateInformationUser.as_view(), name='get-info-user'),
    # ---------------------------
    path('lsit-ad/', ListAdView.as_view(), name='list-ad'),
    path('get-ad/<str:pk>/', GetAdView.as_view(), name='get-ad'),
    path('get-handyman/<str:pk>/', GetHandyMan.as_view(), name='get-handyman'),
    path('list-handyman/', ListHandyMen.as_view(), name='list-handyman'),

    path('create-handman/', CreateHadnyMan.as_view(), name='create-handyman'),
    path('add-service-for-handyman/', AddServiceForHandyManView.as_view(), name='add-service-for-handyman'),
    path('lsit-create-service/', CreateServiceView.as_view(), name='list-create-service'),
    path('get-service/<str:pk>/', GetServiceView.as_view(), name='get-service'),

]
