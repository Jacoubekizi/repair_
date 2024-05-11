from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView , UpdateAPIView ,RetrieveAPIView ,DestroyAPIView
from .serializers import *
from .utils import *
from rest_framework.views import APIView
from rest_framework import status
from .filters import *
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction



class SignUpView(GenericAPIView):
    
    serializer_class  = SignUpSerializer
    def post(self, request):
        user_information = request.data
        serializer = self.get_serializer(data=user_information)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        return Response({'information_user':user_data}, status=status.HTTP_201_CREATED)

# class VerifyAccount(GenericAPIView):

#     def post(self, request, pk):
#         user = CustomUser.objects.filter(pk=pk).first()
#         code = request.data['code']
#         print(code)
#         try:
#             user_code = VerificationCode.objects.get(user=user)
#             print(user_code)
#             if user_code.code == int(code):
#                 if timezone.now() > user_code.expires_at:
#                     return Response("الرجاء اعادة طلب الرمز من جديد نظرا لأن الرمز المدخل انتهت صلاحيته")
#                 user.is_verified = True
#                 user.save()
#                 user_code.delete()
#                 return Response("تم تأكيد حسابك يمكنك الآن المتابعة وتسجيل الدخول")
#         except:
#             return Response("الرجاء اعادة طلب الرمز من جديد")
            

class LoginUser(GenericAPIView):

    def post(self, request):
        serializer = LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = CustomUser.objects.get(email = request.data['username'])
        token = RefreshToken.for_user(user)
        data = serializer.data
        data['image'] = request.build_absolute_uri(user.image.url)
        data['id'] = user.id
        data['tokens'] = {'refresh':str(token), 'access':str(token.access_token)}

        return Response(data, status=status.HTTP_200_OK)
    
class LogoutUser(GenericAPIView):
    serializer_class = LogoutUserSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)
    
class SendCodePassword(GenericAPIView):
    def post(self, request):
        try: 
            email = request.data['email']
            user = get_object_or_404(CustomUser, email=email)
            existing_code = VerificationCode.objects.filter(user=user).first()
            if existing_code:
                existing_code.delete()
            code_verivecation = generate_code()
            code = VerificationCode.objects.create(user=user, code=code_verivecation)
            data= {'to_email':user.email, 'email_subject':'code verify for reset password','username':user.username, 'code': str(code_verivecation)}
            Utlil.send_email(data)
            return Response({'message':'تم ارسال رمز التحقق',
                             'user_id' : user.id})
        except:
            raise serializers.ValidationError("الرجاء ادخال البريد الاكتروني بشكل صحيح")
        
class VerifyCode(GenericAPIView):

    def post(self, request, pk):
        code = request.data['code']
        user = CustomUser.objects.get(id=pk)
        code_ver = VerificationCode.objects.filter(user=user.id).first()
        if code_ver:
            if str(code) == str(code_ver.code):
                if timezone.now() > code_ver.expires_at:
                    return Response("الرجاء اعادة طلب الرمز من جديد نظرا لأن الرمز المدخل انتهت صلاحيته", status=status.HTTP_400_BAD_REQUEST)
                code_ver.is_verified = True
                code_ver.save()
                return Response({"message":"تم التحقق من الرمز", 'user_id':code_ver.user.id},status=status.HTTP_200_OK)
            else:
                return Response('الرمز خاطئ, يرجى إعادة إدخال الرمز بشكل صحيح')
        else:
            return Response("الرجاء اعادة طلب الرمز من جديد")

class ResetPassword(UpdateAPIView):
    serializer_class = ResetPasswordSerializer

    def put(self, request, user_id):
        user = CustomUser.objects.get(id=user_id)
        code = VerificationCode.objects.filter(user=user).first()
        if not code:
            return Response("الرجاء اعادة طلب الرمز من جديد")
        if code.is_verified:
            data = request.data
            serializer = self.get_serializer(data=data, context={'user_id':user_id})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            code.delete()
            messages = {
                'message':'تم تغيير كلمة المرور بنجاح'
            }
            return Response(messages, status=status.HTTP_200_OK)
        
        else:
            return Response({'error':'ليس لديك صلاحية لتغيير كلمة المرور'})
        
class UpdateImagteView(GenericAPIView):
    permission_classes= [IsAuthenticated,]

    def put(self, request):
        data = request.data['image']
        user = CustomUser.objects.get(id=request.user.id)
        user.image = data
        user.save()
        return Response('تم تحديث الصورة الشخصية بنجاح')
    
# class UpdateEmailView(GenericAPIView):
#     permission_classes = [IsAuthenticated,]

#     def put(self, request):
#         email = request.data['email']
#         user = CustomUser.objects.get(id=request.user.id)
#         user.email = email
#         user.is_verified = False
#         user.save()
#         existing_code = VerificationCode.objects.filter(user=user).first()
#         if existing_code:
#             existing_code.delete()
#         code_verivecation = generate_code()
#         code = VerificationCode.objects.create(user=user, code=code_verivecation)
#         data= {'to_email':user.email, 'email_subject':'code verify for verified account','username':user.username, 'code': str(code_verivecation)}
#         Utlil.send_email(data)
#         return Response({'message':'تم ارسال رمز التحقق',
#                             'user_id' : user.id})
    
class RetrieveInfoUser(GenericAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = SerializerInformation

    def get(self, request):
        user = CustomUser.objects.get(id=request.user.id)
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    




class ListCategories(ListAPIView):
    queryset = HandyManCategory
    serializer_class = HandyManCategorySerializer




class AddServiceToCart(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,service_id):
        with transaction.atomic():

            user = CustomUser.objects.get(id=3)## user = request.user

            quantity = request.data.get('quantity')
            client = Client.objects.get(user=user)##
            cart = Cart.objects.get(client=client)
            service = Service.objects.get(id=service_id)
            cart_service , created = CartService.objects.get_or_create(
                service = service.name,
                quantity = quantity,
                cost = service.cost
            )
            cart.service.add(cart_service)

            serializer = CartServiceSerializer(cart_service,many=False)
            return Response(serializer.data,status=status.HTTP_200_OK)




class CreateCartService(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self,request):
        try:
            client = Client.objects.get(id=1)## user = request.user
            user_cart = Cart.objects.get(client=client)
            service_name = request.data['service_name']
            quantity = request.data['quantity']
            cart_service = CartService.objects.create(
                service = service_name,
                quantity = quantity
            )
            user_cart.service.add(cart_service)
            serializer = CartServiceSerializer(cart_service , many=False)
            return Response(serializer.data , status=status.HTTP_200_OK)
        except:
            return Response({"error":"cart does not exist"})





class CartServiceHandler(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self,request,service_id,action):
        try:
            cart_service = CartService.objects.get(id=service_id)
            if action == 'add':
                cart_service.quantity += 1

            elif action == 'sub':
                if cart_service.quantity > 1:
                    cart_service.quantity -= 1
            
            else:
                return Response({"error":"please choose an action"})
                
            cart_service.save()
            serializer = CartServiceSerializer(cart_service,many=False)
            return Response(serializer.data , status=status.HTTP_200_OK)
        except CartService.DoesNotExist:
            return Response({"error":"cart service does not exist"}, status=status.HTTP_200_OK)




class ListCartServices(APIView):
    def get(self,request,cart_id):
        try:
            cart = Cart.objects.get(id=cart_id)
            serializer = CartSerializer(cart , many=False)
            return Response(serializer.data , status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({"error":"cart does not exist"} , status=status.HTTP_404_NOT_FOUND)



class ListAds(ListAPIView):
    queryset = Ad
    serializer_class = AdSerializer




class ListHandyMen(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self,request):
        try:
            handymen = HandyMan.objects.annotate(rating=Avg('review__rating')).order_by('-rating')
            serializer = HandyManSerializer(handymen,many=True , context={"request":request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except HandyMan.DoesNotExist:
            return Response({"error":"there are no handymen available"})
        




class CreateHadnyMan(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        data_handyman = request.data
        serializer = HandyManSerializer(data=data_handyman,many=False , context={"request":request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    




class CityHandymanCount(APIView):
    def get(self, request):
        handymen_by_city = HandyMan.count_handymen_by_city()
        return Response(handymen_by_city)


class GetHandyMan(RetrieveAPIView):
    queryset = HandyMan
    serializer_class = HandyManSerializer




class DeleteOrder(DestroyAPIView):
    queryset = HandyMan
    serializer_class = HandyManSerializer



class AcceptOrder(APIView):
    def post(self,request,order_id):
        try:
            order = Order.objects.get(id=order_id)
            order.accepted = True
            order.save()
            serializer = OrderSerializer(many=False)
            return Response(serializer.data , status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({"error":"order does not exist"})



class CompleteOrder(APIView):
    def post(self,request,order_id):
        try:
            order = Order.objects.get(id=order_id)
            order.completed = True
            order.save()
            serializer = OrderSerializer(many=False)
            return Response(serializer.data , status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({"error":"order does not exist"})




class ListOrders(GenericAPIView):
    queryset = Order
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter

    def get(self,request):
        user = self.request.user
        handyman = HandyMan.objects.get(user=user)
        orders = Order.objects.filter(handy_man=handyman)
        serializer = OrderSerializer(many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    



class ListCalenderOrders(GenericAPIView):
    queryset = Order

    def get(self,request):
        user = self.request.user
        handyman = HandyMan.objects.get(user=user)
        orders = Order.objects.filter(handy_man=handyman)
        serializer = OrderSerializer(many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    
