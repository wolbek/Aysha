from django.db import models
from user.models import User

SIZE_CHOICES = (
    ('XS','XS'),
    ('S','S'),
    ('M','M'),
    ('L','L'),
    ('XL','XL'),
    ('XXL','XXL'),
    ('XXXL','XXXL'),
)

CATEGORY_CHOICES=(
    ('hoodie-male','hoodie-male'),
    ('hoodie-female','hoodie-female'),
    ('sweatshirt-male','sweatshirt-male'),
    ('sweatshirt-female','sweatshirt-female'),
    ('longsleeve-male','longsleeve-male'),
    ('longsleeve-female','longsleeve-female'),
)

class Product(models.Model):
    image = models.ImageField(upload_to='clothing_store/productimg')
    label = models.CharField(max_length=100)
    category = models.CharField(max_length=30,choices=CATEGORY_CHOICES) 
    description = models.TextField()    
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    XS=models.PositiveIntegerField()
    XSprice=models.FloatField()
    S=models.PositiveIntegerField()
    Sprice=models.FloatField()
    M=models.PositiveIntegerField()
    Mprice=models.FloatField()
    L=models.PositiveIntegerField()
    Lprice=models.FloatField()
    XL=models.PositiveIntegerField()
    XLprice=models.FloatField()
    XXL=models.PositiveIntegerField()
    XXLprice=models.FloatField()
    XXXL=models.PositiveIntegerField()    
    XXXLprice=models.FloatField()        

    def _str_(self):
        return str(self.id)
