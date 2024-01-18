from django.shortcuts import render,redirect
from django.views import View
from .forms import Registerform,LoginForm,CardForm
import re
from .models import User,CreditCard
from django.contrib import messages
# from aes.encryption import encrypt_data
from aes.enc import aws_enc
from aes.dec import aws_dec
from django.contrib.auth import authenticate,login,logout
# from aes.rsa import encrypt_data
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class RegisterView(View):
    def get(self,request):
        return render(request,'userdata/register.html',{'form':Registerform()})
    def post(self,request):
        user_data = Registerform(request.POST)
        if user_data.is_valid():
            password = user_data.cleaned_data['password']
            confirm_password = request.POST.get('confirm_password')
            if password != confirm_password:
                user_data.add_error('password', 'Passwords do not match.')
            if not re.match(r'^(?=.*[A-Z])(?=.*\d).{8,}$', password):
                user_data.add_error('password', 'Password should be at least 8 characters long, contain at least one digit and one uppercase letter.')
            if not user_data.errors:
                enc_list=aws_enc(password)
                user=user_data.save(commit=False)
                user.password=enc_list[0]
                user.dek=enc_list[1]
                user.iv=enc_list[2]
                user.save()
                return redirect('userdata:login')
        return render(request, 'userdata/register.html', {'form': user_data})
class LoginView(View):
    def get(self,request):
        return render(request,'userdata/login.html',{'form':LoginForm()})
    def post(self,request):
        login_user=LoginForm(request.POST)
        if login_user.is_valid():
            email=login_user.cleaned_data['email']
            user_enc=User.objects.get(email=email)
            dec_password=aws_dec(user_enc.password,user_enc.dek,user_enc.iv)
            password=login_user.cleaned_data['password']
            if password==dec_password:
                password=user_enc.password
            user=authenticate(request,email=email,password=password)
            if user is not None:
                login(request,user)
                return redirect('userdata:home')
            else:
                login_user.add_error('email','Invalid password or email')
        return render(request,'userdata/login.html',{'form':login_user})
@method_decorator(login_required(login_url='userdata:login'), name='dispatch')
class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('userdata:login')
@method_decorator(login_required(login_url='userdata:login'), name='dispatch')
class AddCardView(View):
    def get(self,request):
        return render(request,'userdata/cardform.html',{'form':CardForm()})
    def post(self,request):
        card_data=CardForm(request.POST)
        if card_data.is_valid():
            number=card_data.cleaned_data['number']
            cvv=card_data.cleaned_data['cvv']
            if not re.match(r'^\d{16}$',number):
                card_data.add_error('number','add number of 16 digit')
            if not re.match(r'^\d{3,4}$',cvv):
                card_data.add_error('cvv','add number of 3 or 4 digit')
            if not card_data.errors:
                credit_card = card_data.save(commit=False)
                credit_card.holder = request.user
                enc_list=aws_enc(number)
                credit_card.number=enc_list[0]
                credit_card.dek=enc_list[1]
                credit_card.iv=enc_list[2]
                credit_card.save()
                messages.success(request, "Card Added Successfully.")
                return redirect('userdata:home')
        return render(request, 'userdata/cardform.html', {'form': card_data})
@method_decorator(login_required(login_url='userdata:login'), name='dispatch')
class HomeView(View):
    def get(self,request):
        cards=CreditCard.objects.filter(holder=request.user)
        creditcard=dict()
        for c in cards:
            number=aws_dec(c.number,c.dek,c.iv)
            creditcard[c.id]={'name':c.name,'number':number,'exp':c.expiration_date,'type':c.type}
        return render(request,'userdata/home.html',{'creditcard':creditcard})