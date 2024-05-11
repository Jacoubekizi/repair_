from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import CustomUser
from django import forms
from django.core.exceptions import ValidationError

class CustomUserCreationForm(forms.ModelForm):

    password1= forms.CharField(label='Password', widget=forms.PasswordInput)
    password2= forms.CharField(label='password confirmatio', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email','phonenumber')

    def clean_password2(self):
        password1=self.cleaned_data.get('password1')
        password2=self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise ValidationError("passwords dont match")
        return password2
    
    def save(self, commit: bool = True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email", 'phonenumber')