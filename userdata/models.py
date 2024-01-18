from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4

card_choice=[['MASTER','Master Card'],['VISA','Visa Card'],['AMEX','American Express']]
class User(AbstractUser):
    id=models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    address = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=100, unique=True)
    age = models.IntegerField()
    iv=models.CharField(max_length=100)
    dek=models.CharField(max_length=1000)
    REQUIRED_FIELDS = ['address', 'phone_no', 'age']
    def __str__(self):
        return self.email
    
class CreditCard(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    holder=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    type=models.CharField(choices=card_choice,max_length=50)
    number=models.CharField(max_length=100)
    cvv=models.CharField(max_length=100)
    expiration_date=models.DateField()
    iv=models.CharField(max_length=100)
    dek=models.CharField(max_length=1000)
    REQUIRED_FIELDS ='__all__'
    def __str__(self) -> str:
        return self.holder.email