from rest_framework import serializers
from django.contrib.auth import  authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import TokenError, RefreshToken
from .models import *

class SignUpSerializer(serializers.ModelSerializer):
    confpassword = serializers.CharField(write_only = True)

    class Meta:
        model = CustomUser
        fields = ['email', 'phonenumber','password', 'confpassword']
        extra_kwargs = {
            'password':{'write_only':True,},
            'confpassword': {'write_only':True}
        }
    def validate(self, validated_data):
        validate_password(validated_data['password'])
        validate_password(validated_data['confpassword'])
        if validated_data['password'] != validated_data['confpassword'] :
            raise serializers.ValidationError("password and confpassword didn't match")
        return validated_data

    def create(self, validated_data):
        validated_data.pop('confpassword', None)
        return CustomUser.objects.create(**validated_data)


class SerializerInformation(serializers.ModelSerializer):

    username = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['email','phonenumber', 'username', 'city','image', 'long', 'lat', 'first_name', 'last_name']

    def get_username(self, obj):
        return f"{obj.first_name} {obj.last_name}"

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only = True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)
            if not user:
                raise serializers.ValidationError("Incorrect Credentials")
            if not user.is_active:
                raise serializers.ValidationError({'message_error':'this account is not active'})
            # if not user.is_verified:
            #     raise serializers.ValidationError({'message_error':'this account is not verified'})
        else:
            raise serializers.ValidationError('Must include "username" and "password".')

        data['user'] = user
        return data
    
    
class LogoutUserSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')

class ResetPasswordSerializer(serializers.Serializer):
    newpassword = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        password = attrs.get('password', '')
        newpassword = attrs.get('newpassword', '')
        validate_password(password)
        validate_password(newpassword)
        if password != newpassword:
            raise serializers.ValidationError('كلمات المرور غير متطابقة')
        
        return attrs

    def save(self, **kwargs):
        user_id = self.context.get('user_id')
        user = CustomUser.objects.get(id=user_id)
        password = self.validated_data['newpassword']
        user.set_password(password)
        user.save()
        return user
    

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class HandyManCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = HandyManCategory
        fields = ['name']

class HandyManSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.username',read_only=True)
    phonenumber = serializers.SerializerMethodField(read_only=True)
    image = serializers.ImageField(source = 'user.image',read_only=True)
    services = ServiceSerializer(many=True, read_only=True)
    category = HandyManCategorySerializer(read_only=True, many=True)

    class Meta:
        model = HandyMan
        fields = ['name', 'phonenumber', 'image', 'services', 'category', 'avg_rating', 'total_reviews']
        

    def get_phonenumber(self,obj):
        return obj.user.phonenumber.as_international
    
    def create(self, validated_data):
        request = self.context.get('request')
        categories = validated_data.pop('category')

        user = CustomUser.objects.get(id=request.user.id)
        instance = HandyMan.objects.create(user=user, **validated_data)
        if categories is not None:
            for category in categories:
                # cat = HandyManCategory.objects.get(id=category)
                instance.category.add(category)
                instance.save()
        return instance
    
class AdSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'