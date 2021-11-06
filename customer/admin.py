from django.contrib import admin
from .models import Order,Cart,CustomerAddress
# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display=['customer_id','product_id','save_quantity','product_size','price']
    def has_add_permission(self, request, obj=None):
        return False
    
    
admin.site.register(Cart,CartAdmin)

class CustomerAddressAdmin(admin.ModelAdmin):
    list_display=['customer','firstname','lastname','address']
    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(CustomerAddress,CustomerAddressAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display=['customer_id','customer_firstname','customer_lastname','product_id','product_label','product_size','buy_quantity','price','shippingprice','to_address','order_date','delivery_date','delivered_date','delivery_status','seller_id']
    def has_add_permission(self, request, obj=None):
        return False
    

admin.site.register(Order,OrderAdmin)

