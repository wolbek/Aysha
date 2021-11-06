from django.urls import path
from . import views

app_name='customer'

urlpatterns = [   
    path('signupcustomer/',views.signupcustomer,name='signupcustomer'),  
    path('logincustomer/',views.logincustomer,name='logincustomer'), 
    path('logoutcustomer/',views.logoutcustomer,name='logoutcustomer'),

    path('addaddress/',views.addaddress,name="addaddress"),
    path('savedaddress/',views.savedaddress,name="savedaddress"),
    path('changepassword/',views.changepassword,name='changepassword'),

    path('productdetail/<int:product_pk>',views.productdetail,name='productdetail'),
    path('api/instock',views.instock,name="instock"),
    path('api/incart',views.incart,name="incart"),
    path('api/instockornot',views.instockornot,name="instockornot"),

    path('addtocart/<int:product_pk>',views.addtocart,name='addtocart'),
    path('cart/',views.cart,name="cart"),

    path('contactus/',views.contactus,name='contactus'),
    path('thankyou/',views.thankyou,name='thankyou'),
  
    path('api/removeitem',views.removeitem,name="removeitem"),
    path('api/deleteaddress',views.deleteaddress,name="deleteaddress"),

    path('hoodiemen/',views.hoodiemen,name='hoodiemen'),
    path('sweatshirtmen/',views.sweatshirtmen,name='sweatshirtmen'),
    path('longsleevemen/',views.longsleevemen,name='longsleevemen'),

    path('hoodiewomen/',views.hoodiewomen,name='hoodiewomen'),
    path('sweatshirtwomen/',views.sweatshirtwomen,name='sweatshirtwomen'),
    path('longsleevewomen/',views.longsleevewomen,name='longsleevewomen'),
    # For search bar list items when anything is typed on searchbar
    path('api/productlist',views.productlist,name='productlist'),
    # To show the searched product when search button is clicked
    path('searchresultproduct/',views.searchresultproduct, name='searchresultproduct'),

    path('orderhistory/',views.orderhistory,name='orderhistory'),

    #To show products when filter tab is used
    path('api/filteredresult',views.filteredresult,name='filteredresult'),

    path('ordersummary/',views.ordersummary,name='ordersummary'),
    path('singleordersummary/<int:product_pk>',views.singleordersummary,name='singleordersummary'),

    path('paymentsuccess/',views.paymentsuccess,name='paymentsuccess'),
    path('singlepaymentsuccess/',views.singlepaymentsuccess,name='singlepaymentsuccess'),




]