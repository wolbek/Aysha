from django.contrib import admin
from seller.models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display=['id','user','label','category','description','XS','S','M','XL','XXL','XXXL']
    def has_add_permission(self, request, obj=None):
        return False
    
    

admin.site.register(Product,ProductAdmin)