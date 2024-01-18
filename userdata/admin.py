from django.contrib import admin
from .models import User,CreditCard
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display=['email','age','phone_no','address','iv','dek']
@admin.register(CreditCard)
class AdminCreditCard(admin.ModelAdmin):
    list_display=['holder','name','type','number','cvv','expiration_date','iv','dek']