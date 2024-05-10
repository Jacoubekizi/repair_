from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField
# from django.contrib.gis.geos import Point
# from django.contrib.gis.db import models
from .utils import *
from .options import *
# from fcm_django.models import FCMDevice
# from firebase_admin.messaging import Message
# from firebase_admin.messaging import Notification as FirebaseNotification


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=50, unique=True)
    phonenumber = PhoneNumberField(region='SY', blank = True, null = True)
    # country = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to='images/users',default='images/account. ')
    # country = models.PointField(null=True,blank=True)

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ('username',)

    def __str__(self) -> str:
        return self.username

    class Meta:
        ordering = ['-id']
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class VerificationCode(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    code = models.IntegerField(validators=[MinValueValidator(1000), MaxValueValidator(9999)])
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=get_expiration_time)

    def __str__(self):
        return f'{self.user.username} code:{self.code}'
    
class Handyman(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.username
    

class Service(models.Model):
    name = models.CharField(max_length=100)
    cover = models.ImageField(upload_to='images/service')
    handyman = models.ManyToManyField(Handyman)

    def __str__(self) -> str:
        return f"{self.name}-{self.handyman.user.username}"
    
class Governorate(models.Model):
    name = models.CharField(choices=Governorate_Name)
    handyman = models.ForeignKey(Handyman)

    def __str__(self) -> str:
        return self.name
    
class Poster(models.Model):
    cover = models.ImageField(upload_to='images/poster')
    descreption = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return str(self.id)

class Gategories(models.Model):
    name = models.CharField(max_length=100)
    cover = models.ImageField(upload_to='images/categories')
    handyman = models.ManyToManyField(Handyman)

    def __str__(self) -> str:
        return self.name