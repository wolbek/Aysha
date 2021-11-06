from django.forms import ModelForm
from customer.models import Order

class OrderForm(ModelForm):
    class Meta:
        model=Order
        readonly_fields=('order_datetime',)
        fields=['customer_firstname','customer_lastname','product_label','product_size','buy_quantity','to_address','delivery_date','delivery_status']


