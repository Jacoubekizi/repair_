from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.generics import *
from .serializers import *
from .utils import *


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
    

# ----------------------------------------------------------------
class ListHandymanView(ListAPIView):
    serializer_class = HandymanSerializer
    queryset = Handyman.objects.all()
    permission_classes = [IsAuthenticated,]


class ListGovernorateView(ListAPIView):
    serializer_class = GovernorateSerializer
    queryset = Governorate.objects.all()
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        governorate_with_handyman_count = Governorate.objects.annotate(handyman_count=Count('hanyman')).order_by('-handyman_count')
        return governorate_with_handyman_count[:6]
    

class ListHandymanView(ListAPIView):
    serializer_class = HandymanSerializer
    queryset = Handyman.objects.all()
    permission_classes = [IsAuthenticated,]