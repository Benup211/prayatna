from django import forms
from .models import User,CreditCard
class Registerform(forms.ModelForm):
    confirm_password=forms.PasswordInput(attrs={'class': 'form-control'})
    class Meta:
        model=User
        fields=['username','email','address','phone_no','age','password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        help_texts={
            'username':None
        }
class LoginForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['email','password']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
class CardForm(forms.ModelForm):
    class Meta:
        model=CreditCard
        fields=['name','type','number','cvv','expiration_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'type': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select card type'}),
            'number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter card number','type':'number','min':'1000000000000000','max':'9999999999999999'}),
            'cvv': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter CVV:1234','type':'number','min':'100','max':'9999'}),
            'expiration_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Enter expiration date','type':'date'}),
        }