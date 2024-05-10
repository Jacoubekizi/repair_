from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from .utils import *
# from fcm_django.models import FCMDevice
# from firebase_admin.messaging import Message
# from firebase_admin.messaging import Notification as FirebaseNotification
from django.db.models import Avg




class CustomUser(AbstractUser):
    email = models.EmailField(max_length=50, unique=True)
    phonenumber = PhoneNumberField(region='SY', blank = True, null = True)
    image = models.ImageField(upload_to='images/users',default='images/account.png')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username','phonenumber')

    def __str__(self) -> str:
        return self.username

    class Meta:
        ordering = ['-id']



class VerificationCode(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    code = models.IntegerField(validators=[MinValueValidator(1000), MaxValueValidator(9999)])
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=get_expiration_time)

    def __str__(self):
        return f'{self.user.username} code:{self.code}'
    



class Client(models.Model):
    user = models.ForeignKey(CustomUser , on_delete=models.CASCADE)### or one2one field
    name = models.CharField(max_length=100)
    # location = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.user.username


class HandyManCategory(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name



class Ad(models.Model):
    image = models.ImageField(upload_to='')
    description = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.description




class PopularCity(models.Model):
    description = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name



class Review(models.Model):
    author = models.ForeignKey(Client , on_delete=models.CASCADE)
    handyman = models.ForeignKey('HandyMan' , on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1) , MaxValueValidator(5)])
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.author} : {self.rating}'



class Service(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/services' , default='images/default.png')
    cost = models.IntegerField()

    def __str__(self) -> str:
        return self.name




class CartService(models.Model):
    service = models.ForeignKey(Service , on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart' , on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.service} - {self.quantity}'



class Cart(models.Model):
    services = models.ManyToManyField(Service , through='CartService')
    client = models.OneToOneField(Client , on_delete=models.CASCADE)



class HandyMan(models.Model):
    user = models.ForeignKey(CustomUser , on_delete=models.CASCADE)
    category = models.ForeignKey(HandyManCategory , on_delete=models.CASCADE)
    # name = models.CharField(max_length=100)
    location = models.CharField(max_length=50)
    services = models.ManyToManyField(Service)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def avg_rating(self):
        return self.review_set.only('rating').aggregate(Avg('rating'))['rating__avg']
    
    @property
    def total_reviews(self):
        return self.review_set.count()

    def __str__(self) -> str:
        return self.name
    



class Order(models.Model):
    handy_man = models.ForeignKey(HandyMan , on_delete=models.CASCADE)
    client = models.ForeignKey(Client , on_delete=models.CASCADE)
    service = models
    accepted = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self) -> str:
        return 

     
