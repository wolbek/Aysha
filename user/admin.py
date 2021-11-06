from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import User,Seller,Customer

@admin.register(User)
class UserAdmin(DjangoUserAdmin):

    fieldsets = (
        (None, {'fields': ('email', 'password')}), 
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser','is_seller','is_customer','groups', 'user_permissions')}), 
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email','is_seller','is_customer','is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    def has_add_permission(self, request, obj=None):
        return False

class SellerAdmin(admin.ModelAdmin):
    list_display=['user','shopname','phoneno','warehouselocation']
    def has_add_permission(self, request, obj=None):
        return False   

class CustomerAdmin(admin.ModelAdmin):
    list_display=['user','gender','phoneno'] 
    def has_add_permission(self, request, obj=None):
        return False    

admin.site.register(Seller,SellerAdmin)
admin.site.register(Customer,CustomerAdmin)
