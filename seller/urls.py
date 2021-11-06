from django.urls import path
from . import views

app_name='seller'

urlpatterns = [   
    path('signupseller/',views.signupseller,name='signupseller'),
    path('loginseller/',views.loginseller,name='loginseller'),
    path('logoutseller/',views.logoutseller,name='logoutseller'),
    path('dashboard/',views.dashboard,name='dashboard'),    
    path('createproduct/',views.createproduct,name='createproduct'),
    path('changepassword/',views.changepassword,name='changepassword'), 
    path('inventory/',views.inventory,name='inventory'), 
    path('editproduct/<int:product_pk>',views.editproduct,name='editproduct'), 
    path('deleteproduct/',views.deleteproduct,name='deleteproduct'), 
    path('api/productlist/',views.productlist,name='productlist'),
    path('orderpending/',views.orderpending,name='orderpending'), 
    path('ordercompleted/',views.ordercompleted,name='ordercompleted'), 
    path('analytic/',views.analytic,name='analytic'), 
    path('api/orderlist/',views.orderlist,name='orderlist'),
    path('api/completedorderlist/',views.completedorderlist,name='completedorderlist'),
   
    path('genderchart/',views.genderchart,name='genderchart'),
    path('productdata/',views.productdata,name='productdata'),

    path('emailregistered/',views.emailregistered,name='emailregistered')
]