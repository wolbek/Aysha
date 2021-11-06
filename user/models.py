# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from .managers import UserManager

class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    is_seller = models.BooleanField('seller status', default=False)
    is_customer = models.BooleanField('customer status', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
    
    def __str__(self):
        return self.email

class Seller(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    phoneno=models.CharField(max_length=12,null=True)   
    shopname=models.CharField(max_length=50,null=True)
    warehouselocation=models.CharField(max_length=300,null=True)

GENDER_CHOICES = (
    ('M','Male'),
    ('F','Female'),
)

class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)  
    gender=models.CharField(max_length=10,choices=GENDER_CHOICES)
    phoneno=models.CharField(max_length=12,null=True)     
    


