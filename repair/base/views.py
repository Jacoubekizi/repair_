from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView , UpdateAPIView ,RetrieveAPIView ,DestroyAPIView, ListCreateAPIView
from .serializers import *
from .utils import *
from rest_framework.views import APIView
from rest_framework import status
from .filters import *
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from datetime import date



class SignUp(GenericAPIView):
    
    serializer_class  = SignUpSerializer
    def post(self, request):
        user_information = request.data
        serializer = self.get_serializer(data=user_information)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = CustomUser.objects.get(email=user_information['email'])
        token = RefreshToken.for_user(user)
        user_data = serializer.data
        user_data['tokens'] = {'refresh':str(token), 'access':str(token.access_token)}
        return Response({'information_user':user_data}, status=status.HTTP_201_CREATED)





class SignUpClient(GenericAPIView):
    serializer_class  = SignUpSerializer
    
    def post(self, request):
        user_information = request.data
        serializer = self.get_serializer(data=user_information)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = CustomUser.objects.get(email=user_data['email'])
        client = Client.objects.create(user=user)
        cart = Cart.objects.create(client=client)
        return Response({'information_user':user_data}, status=status.HTTP_201_CREATED)

       

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





class UpdateUserInfo(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = CustomUser.objects.get(id=request.user.id)
        data = request.data
        user.email=data['email']
        user.phonenumber = data['phonenumber']
        user.last_name = data['last_name']
        user.first_name = data['first_name']
        user.save()
        return Response('تم تحديث البيانات بنجاح')


class RetrieveUserInfo(GenericAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = SerializerInformation

    def get(self, request):
        user = CustomUser.objects.get(id=request.user.id)
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    




class ListCreateServices(ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request']=self.request
        return context




class GetInfoHandyman(GenericAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = InfoHandymanSerializer

    def get(self, request):
        handyman = HandyMan.objects.get(user=request.user)
        serializer = self.get_serializer(handyman)
        return Response(serializer.data)

class GetService(RetrieveAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer





class ListCategories(ListAPIView):
    queryset = HandyManCategory.objects.all()
    serializer_class = HandyManCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request']=self.request
        return context


class AssignCategory(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,pk):
        try:
            category = HandyManCategory.objects.get(id=pk)
            print(category)
            handyman = HandyMan.objects.get(user=request.user)
            # if category in handyman.category.all():
            if handyman.category.filter(name=category.name).exists():
                handyman.category.remove(category)
            else:
                handyman.category.add(category)

            serializer = HandyManSerializer(handyman , many=False, context={'request':request})
            return Response(serializer.data , status=status.HTTP_200_OK)

        except HandyManCategory.DoesNotExist:
            return Response({"error":"category does not exist"} , status=status.HTTP_404_NOT_FOUND)


class AssignService(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,pk):
        try:
            servrice = Service.objects.get(id=pk)
            handyman = HandyMan.objects.get(user=request.user)
            if handyman.services.filter(name=servrice.name).exists():
                handyman.services.remove(servrice)
            else:
                handyman.services.add(servrice)

            serializer = HandyManSerializer(handyman , many=False, context={'request':request})
            return Response(serializer.data , status=status.HTTP_200_OK)

        except Service.DoesNotExist:
            return Response({"error":"category does not exist"} , status=status.HTTP_404_NOT_FOUND)

class AddServiceToCart(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,service_id):
        with transaction.atomic():
            quantity = request.data.get('quantity')
            client = Client.objects.get(user=request.user)
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
            client = Client.objects.get(user=request.user)
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

class ResetCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        client = Client.objects.get(user=user)
        cart = Cart.objects.get(client=client)
        cart.service.clear()
        cart.date = None
        cart.time = None
        cart.save()
        return Response(status=status.HTTP_200_OK)



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




class SetDateTimeCart(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        with transaction.atomic():
            try:
                client = Client.objects.get(user=request.user)
                cart = Cart.objects.get(client=client)
                day = int(request.data['day'])
                month = int(request.data['month'])
                year = int(request.data['year']) 
                time = request.data['time']

                cart_date = date(year,month,day)
                cart.date = cart_date
                cart.time = time
                cart.save()

                serializer = CartSerializer(cart,many=False)
                return Response(serializer.data , status=status.HTTP_200_OK)
            
            except Client.DoesNotExist or Cart.DoesNotExist:
                return Response({"error":"client or cart does not exist"} , status=status.HTTP_404_NOT_FOUND)





class CreateOrder(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,handy_man_id):
        with transaction.atomic():
            try:
                
                handy_man = HandyMan.objects.get(id=handy_man_id)
                client = Client.objects.get(user=request.user)
                cart = Cart.objects.get(client=client)
                order = Order.objects.create(
                    handy_man = handy_man,
                    client = client,
                    date = cart.date,
                    time = cart.time,
                )
                for service in cart.service.all():
                    order_service = OrderService.objects.create(
                        service = service,
                        quantity = int(service.quantity),
                        cost = int(service.cost)
                    )
                    order.service.add(order_service)
                order.save()
                cart.service.clear()
                cart.date = None
                cart.time = None
                cart.save()
                # b = Order.objects.get(id=order.id)
                serializer = OrderSerializer(order , many=False)
                return Response(serializer.data , status=status.HTTP_200_OK)
            except Exception as e:
                return Response( {'message':str(e)}, status=status.HTTP_404_NOT_FOUND)


class ListCartServices(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        try:
            user = request.user
            client = Client.objects.get(user=user)
            cart = Cart.objects.get(client=client)
            serializer = CartSerializer(cart , many=False)
            return Response(serializer.data , status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({"error":"cart does not exist"} , status=status.HTTP_404_NOT_FOUND)



class ListAds(ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer



class GetAd(RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer




class ListHandyMen(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        try:
            handymen = HandyMan.objects.annotate(rating=Avg('review__rating')).order_by('-rating')
            serializer = HandyManSerializer(handymen,many=True , context={"request":request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except HandyMan.DoesNotExist:
            return Response({"error":"there are no handymen available"})
        


class CreateHadnyMan(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data_handyman = request.data
        serializer = HandyManSerializer(data=data_handyman,many=False , context={"request":request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)



class GetHandyMan(RetrieveAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = HandyMan
    serializer_class = HandyManSerializer



class CityHandymanCount(APIView):
    def get(self, request):
        handymen_by_city = HandyMan.count_handymen_by_city()
        return Response(handymen_by_city)




class DeleteOrder(DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer



class AcceptOrder(APIView):
    def post(self,request,order_id):
        try:
            order = Order.objects.get(id=order_id)
            order.accepted = True
            order.save()
            serializer = OrderSerializer(order,many=False)
            return Response(serializer.data , status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({"error":"order does not exist"})



class CompleteOrder(APIView):
    def post(self,request,order_id):
        try:
            order = Order.objects.get(id=order_id)
            order.completed = True
            order.save()
            serializer = OrderSerializer(order,many=False)
            return Response(serializer.data , status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({"error":"order does not exist"})




class ListOrders(GenericAPIView):
    queryset = Order
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = request.user
        handyman = HandyMan.objects.get(user=user)
        orders = handyman.order_set.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    



class ListCalenderOrders(GenericAPIView):
    queryset = Order

    def get(self,request):
        user = self.request.user
        handyman = HandyMan.objects.get(user=user)
        orders = Order.objects.filter(handy_man=handyman)
        serializer = OrderSerializer(many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    


class ListReviews(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewFilter


class CreateReviewsView(GenericAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, handy_man_id):
        handy_man = HandyMan.objects.get(id=handy_man_id)
        # client = Client.objects.get(user=request.user)
        review = Review.objects.create(user=request.user, handyman=handy_man, rating=request.data['rating'])
        serializer = self.get_serializer(review, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class GetReview(RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer