
from django.db import models
from seller.models import Product
from user.models import User,Seller,Customer
# Create your models here.

SIZE_CHOICES=(
    ('XS','XS'),
    ('S','S'),
    ('M','M'),
    ('L','L'),
    ('XL','XL'),
    ('XXL','XXL'),
    ('XXXL','XXXL')
)

STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel')
)

class Cart(models.Model):
    customer=models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    save_quantity = models.PositiveIntegerField(default=1)
    product_size=models.CharField(max_length=5,choices=SIZE_CHOICES)
    price=models.FloatField(default=0)
    

    def _str_(self):
        return str(self.id)
    

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Customer')
    customer_firstname=models.CharField(max_length=50)  
    customer_lastname=models.CharField(max_length=50)  
    product= models.ForeignKey(Product,on_delete=models.CASCADE)
    product_label=models.CharField(max_length=100)  
    seller = models.ForeignKey(User,on_delete=models.CASCADE,related_name='Seller')   
    product_size=models.CharField(max_length=5,choices=SIZE_CHOICES)
    buy_quantity = models.PositiveIntegerField(default=1)    
    to_address = models.CharField(max_length=300)  
    order_date= models.DateField(null=True,blank=True)
    delivered_date=models.DateField(null=True,blank=True)
    delivery_date = models.DateField(null=True,blank=True)
    delivery_status = models.CharField(max_length=30,choices=STATUS_CHOICES,default='Pending')
    price=models.FloatField(default=0)     
    shippingprice=models.FloatField(default=100)  
    # shipment_charges = models.FloatField()
    def _str_(self):
        return str(self.id)

class CustomerAddress(models.Model):
    customer=models.ForeignKey(User, on_delete=models.CASCADE)
    firstname=models.CharField(max_length=50)  
    lastname=models.CharField(max_length=50)
    address=models.CharField(max_length=300,null=True)

    def _str_(self):
        return str(self.id)

