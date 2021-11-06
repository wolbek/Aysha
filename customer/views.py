from typing import Sized
from django.shortcuts import render

import datetime
from django.http import HttpResponseRedirect

# from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from user.models import Customer, User,Seller
from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate, update_session_auth_hash
from django.db import IntegrityError
from django.contrib import messages
from user.forms import ChangePasswordForm
from seller.models import Product
from customer.models import Cart,CustomerAddress,Order
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from seller.serializers import ProductSerializer,OrderSerializer

import razorpay

from itertools import chain

# Create your views here.

def home(request):
    menproducts1=Product.objects.filter(category='hoodie-male').order_by('-id')[:3]
    menproducts2=Product.objects.filter(category='sweatshirt-male').order_by('-id')[:4]
    menproducts3=Product.objects.filter(category='longsleeve-male').order_by('-id')[:3] 
    menproducts = list(chain(menproducts1, menproducts2, menproducts3))

    womenproducts1=Product.objects.filter(category='hoodie-female').order_by('-id')[:3]
    womenproducts2=Product.objects.filter(category='sweatshirt-female').order_by('-id')[:4]
    womenproducts3=Product.objects.filter(category='longsleeve-female').order_by('-id')[:3]    
    womenproducts = list(chain(womenproducts1, womenproducts2, womenproducts3))

    return render(request,'customer/home.html',{'menproducts':menproducts,'womenproducts':womenproducts})

def signupcustomer(request):  

    if request.method=='GET':
            return render(request,'customer/signupcustomer.html')
    else:
        user=User.objects.create_user(request.POST['email'],request.POST['password1'],is_customer=True)
        Customer.objects.create(user=user,gender=request.POST['gender'],phoneno=request.POST['phoneno'])
        # customer=get_object_or_404(User,email=request.POST['email'])
        # CustomerAddress(customer=customer,firstname=request.POST['firstname'],lastname=request.POST['lastname'],address=request.POST['addressline1']+", "+request.POST['addressline2']+", "+request.POST['city']+", "+request.POST['state']+", "+request.POST['pincode']).save()
        login(request,user)
        return redirect('home')      


def logincustomer(request):
    if request.method=='GET':
        return render(request,'customer/logincustomer.html')
    else:
        user=authenticate(request,email=request.POST['email'],password=request.POST['password'])

        if user is None or user.is_customer==False:
            messages.error(request,'Username and Password did not match')
            return render(request,'customer/logincustomer.html')
        else:
            login(request,user)            
            return redirect('home')

def logoutcustomer(request):
    if request.method=='POST':
        logout(request)
        return redirect('home')

def productdetail(request,product_pk):
    product=get_object_or_404(Product,pk=product_pk)
    seller=get_object_or_404(Seller,user=product.user)   
    return render(request,'customer/productdetail.html',{'product':product,'sellershopname':seller.shopname})
    
@api_view(['GET'])
def instock(request):   
    product=get_object_or_404(Product,pk=request.GET['pid']) 
    available=""  
    if request.GET['size']=="XS":
        productsizecount=product.XS    
    elif request.GET['size']=="S":
        productsizecount=product.S    
    elif request.GET['size']=="M":
        productsizecount=product.M     
    elif request.GET['size']=="L":
        productsizecount=product.L        
    elif request.GET['size']=="XL":
        productsizecount=product.XL      
    elif request.GET['size']=="XXL":
        productsizecount=product.XXL   
    elif request.GET['size']=="XXXL":
        productsizecount=product.XXXL

    if productsizecount>10:
        available="IN STOCK"
    elif 1<=productsizecount<=10:
        available="Currently "+str(productsizecount)+" items are available"
    elif productsizecount==0:
        available="OUT OF STOCK"

    return JsonResponse({'available':available})

@api_view(['GET'])
def incart(request):   
    cartitem=Cart.objects.filter(customer=request.user,product=request.GET['pid'],product_size=request.GET['size'])
    incart=False
    if not cartitem:
        incart=False
    else:
        incart=True
    return JsonResponse({'incart':incart})

def addtocart(request,product_pk):   
    
    product=get_object_or_404(Product,pk=product_pk)
    if request.POST['productsize']=="XS":
        price=get_object_or_404(Product,pk=product_pk).XSprice
    elif request.POST['productsize']=="S":
        price=get_object_or_404(Product,pk=product_pk).Sprice
    elif request.POST['productsize']=="M":
        price=get_object_or_404(Product,pk=product_pk).Mprice
    elif request.POST['productsize']=="L":
        price=get_object_or_404(Product,pk=product_pk).Lprice
    elif request.POST['productsize']=="XL":
        price=get_object_or_404(Product,pk=product_pk).XLprice
    elif request.POST['productsize']=="XXL":
        price=get_object_or_404(Product,pk=product_pk).XXLprice
    elif request.POST['productsize']=="XXXL":
        price=get_object_or_404(Product,pk=product_pk).XXXLprice
    
    customer=get_object_or_404(User,email=request.user)

    Cart(customer=customer, product=product,product_size=request.POST['productsize'],price=price).save()
    messages.success(request,'Product Added To Cart Successfully')
    return redirect('customer:cart')
    


def cart(request):   
    cartitems=Cart.objects.filter(customer=request.user).order_by('-id')
    return render(request,'customer/cart.html',{'cartitems':cartitems,'totalprice':totalprice(request),'totalitems':totalitems(request)})
    # Should we use ajax and jsonresponse here to increment and decrement save_quantity or make a different function?

@api_view(['POST'])
def instockornot(request):    
    cartitem=get_object_or_404(Cart,pk=request.POST['pid'])  
    # Plus cannot add more than what is in database
    product=get_object_or_404(Product,pk=cartitem.product.id)
    productsizecount=""
    available=""
    # To store available number of product of this size
    if request.POST['productsize']=="XS":
        productsizecount=product.XS
    elif request.POST['productsize']=="S":
        productsizecount=product.S
    elif request.POST['productsize']=="M":
        productsizecount=product.M
    elif request.POST['productsize']=="L":
        productsizecount=product.L
    elif request.POST['productsize']=="XL":
        productsizecount=product.XL
    elif request.POST['productsize']=="XXL":
        productsizecount=product.XXL
    elif request.POST['productsize']=="XXXL":
        productsizecount=product.XXXL
    
    # To know if current selected amount is in stock or not
    

    if(request.POST['change']=="plus"):

        if cartitem.save_quantity+1>productsizecount:
            available="Currently only "+str(productsizecount)+" items are available"
        elif cartitem.save_quantity+1<=productsizecount:
            available="IN STOCK"
        elif productsizecount==0:
            available="OUT OF STOCK"

        cartitem.save_quantity+=1
        cartitem.save()

    elif(request.POST['change']=="minus"):

        if cartitem.save_quantity-1>productsizecount:
            available="Currently only "+str(productsizecount)+" items are available"
        elif cartitem.save_quantity-1<=productsizecount:
            available="IN STOCK"
        elif productsizecount==0:
            available="OUT OF STOCK"

        cartitem.save_quantity-=1
        cartitem.save()     
    
    elif(request.POST['change']=="none"):
        if cartitem.save_quantity>productsizecount:
            available="Currently only "+str(productsizecount)+" items are available"
        elif cartitem.save_quantity<=productsizecount:
            available="IN STOCK"
        elif productsizecount==0:
            available="OUT OF STOCK"

    return JsonResponse({'available':available,'totalprice':totalprice(request),'totalitems':totalitems(request)})

@api_view(['POST'])
def removeitem(request):
    cartitem=Cart.objects.filter(pk=request.POST['pid'])   
    cartitem.delete()
    return JsonResponse({'status':1,'totalprice':totalprice(request),'totalitems':totalitems(request),'message':"Product Removed Successfully"})


def totalprice(request):
    cartitems=Cart.objects.filter(customer=request.user)
    total=0
    for i in cartitems:
        total+=i.price*i.save_quantity
    return float(total)

def totalitems(request):
    cartitems=Cart.objects.filter(customer=request.user)
    total=0
    for i in cartitems:
        total+=i.save_quantity
    return total


def contactus(request):
    return render(request,'customer/contactus.html')

def thankyou(request):
    return render(request,'customer/thankyou.html')

def changepassword(request):    
    if request.method=='GET':  
        return render(request,'customer/changepassword.html',{'form':ChangePasswordForm(user=request.user)})
    else:
        form=ChangePasswordForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            messages.success(request,'Password changed successfully')
            return HttpResponseRedirect(request.path_info)
        else:
            messages.error(request, form.errors)
            # messages.error(request, 'Not a valid password')

            return render(request,'customer/changepassword.html',{'form':ChangePasswordForm(user=request.user),'error':True})

def savedaddress(request):
    customeraddresses=CustomerAddress.objects.filter(customer=request.user)
    return render(request,'customer/savedaddress.html',{'customeraddresses':customeraddresses})

def addaddress(request):
    if request.method=="GET":        
        if(request.GET['frompage']=="savedaddress"):
            return render(request,'customer/addaddress.html',{'savedaddress':True})
        elif(request.GET['frompage']=="ordersummary"):
            return render(request,'customer/addaddress.html',{'ordersummary':True})
    else:
        customer=get_object_or_404(User,email=request.user)
        CustomerAddress(customer=customer,firstname=request.POST['firstname'],lastname=request.POST['lastname'],address=request.POST['addressline1']+", "+request.POST['addressline2']+", "+request.POST['city']+", "+request.POST['state']+", "+request.POST['pincode']).save()
        
        if request.POST['frompage']=="savedaddress":
            messages.success(request,'Address Added Successfully')
            return redirect('customer:savedaddress')
        elif request.POST['frompage']=="ordersummary":
            messages.success(request,'Address Added Successfully')
            return redirect('customer:ordersummary')  

@api_view(['POST'])
def deleteaddress(request):
    address=CustomerAddress.objects.filter(pk=request.POST['aid'])
    address.delete()
    return JsonResponse({'status':1})

    # Categoydatabase has the category value as stored in database which we will use to find filtered result

def hoodiemen(request):
    result=Product.objects.filter(category='hoodie-male').order_by('-id')
    return render(request,'customer/selectedcategory.html',{'result':result,'category':'Hoodies (Men)','categorydatabase':'hoodie-male'})

def sweatshirtmen(request):
    result=Product.objects.filter(category='sweatshirt-male').order_by('-id')
    return render(request,'customer/selectedcategory.html',{'result':result,'category':'Sweatshirts (Men)','categorydatabase':'sweatshirt-male'})

def longsleevemen(request):
    result=Product.objects.filter(category='longsleeve-male').order_by('-id')
    return render(request,'customer/selectedcategory.html',{'result':result,'category':'Longsleeves (Men)','categorydatabase':'longsleeve-male'})

def hoodiewomen(request):
    result=Product.objects.filter(category='hoodie-female').order_by('-id')
    return render(request,'customer/selectedcategory.html',{'result':result,'category':'Hoodies (Women)','categorydatabase':'hoodie-female'})

def sweatshirtwomen(request):
    result=Product.objects.filter(category='sweatshirt-female').order_by('-id')
    return render(request,'customer/selectedcategory.html',{'result':result,'category':'Sweatshirts (Women)','categorydatabase':'sweatshirt-female'})

def longsleevewomen(request):
    result=Product.objects.filter(category='longsleeve-female').order_by('-id')
    return render(request,'customer/selectedcategory.html',{'result':result,'category':'Longsleeves (Women)','categorydatabase':'longsleeve-female'})

@api_view(['GET'])
def productlist(request):
    # Will show top 11 items in search list because showing all will take space, and when user gets more specific he will definitly find his item (if item exists) within 11 items at top
    products=Product.objects.filter(label__icontains=request.GET['searchcontent']).order_by('-id')[:11]
    serializer=ProductSerializer(products,many=True) 
    return Response(serializer.data)

def searchresultproduct(request):    
    result=Product.objects.filter(label__icontains=request.POST['searchcontent']).order_by('-id')
    return render(request,'customer/selectedcategory.html',{'result':result,'searchcontent':request.POST['searchcontent']})

def orderhistory(request):
    customer=get_object_or_404(User,email=request.user)
    orders=Order.objects.filter(customer=customer).order_by('-id')
    return render(request,'customer/orderhistory.html',{'orders':orders})

@api_view(['GET'])
def filteredresult(request):
    # print("------------------")
    # print(request.GET['category'])
    # print(request.GET['searchcontent'])
    if request.GET['category']=="":
        if request.GET['sortby']=='newest':
            products=Product.objects.filter(label__icontains=request.GET['searchcontent']).order_by('-id')
        elif request.GET['sortby']=='price-low-to-high':
            products=Product.objects.filter(label__icontains=request.GET['searchcontent']).order_by('Mprice')
        elif request.GET['sortby']=='price-high-to-low':
            products=Product.objects.filter(label__icontains=request.GET['searchcontent']).order_by('-Mprice')
        elif request.GET['sortby']=='name-A-Z':
            products=Product.objects.filter(label__icontains=request.GET['searchcontent']).order_by('label')
        elif request.GET['sortby']=='name-Z-A':
            products=Product.objects.filter(label__icontains=request.GET['searchcontent']).order_by('-label')
    if request.GET['searchcontent']=="":
        if request.GET['sortby']=='newest':
            products=Product.objects.filter(category=request.GET['category']).order_by('-id')
        elif request.GET['sortby']=='price-low-to-high':
            products=Product.objects.filter(category=request.GET['category']).order_by('Mprice')
        elif request.GET['sortby']=='price-high-to-low':
            products=Product.objects.filter(category=request.GET['category']).order_by('-Mprice')
        elif request.GET['sortby']=='name-A-Z':
            products=Product.objects.filter(category=request.GET['category']).order_by('label')
        elif request.GET['sortby']=='name-Z-A':
            products=Product.objects.filter(category=request.GET['category']).order_by('-label')
    serializer=ProductSerializer(products,many=True) 
    return Response(serializer.data)

def ordersummary(request):
    cartitems=Cart.objects.filter(customer=request.user).order_by('-id')
    customeraddresses=CustomerAddress.objects.filter(customer=request.user)
    amount=totalprice(request)+100
    customer=get_object_or_404(Customer,user=request.user)
    
    client = razorpay.Client(auth=("rzp_test_5T9IAkXd2Zeh6q", "4jtzAZkCev9udXHdA99mlcNj"))
    data={
        "amount" : amount*100,
        "currency" : 'INR',
        "receipt" : 'receipt55',
        "notes" : {        
                    # 'name':customer.firstname+" "+customer.lastname,           
                    'email': customer.user.email,
                    'phone':customer.phoneno,                    
                  } 
    }
    
    # We create an order with the data.
    order=client.order.create(data=data) 
    #Order is an object. We pass this as dictionary        
    return render(request,'customer/ordersummary.html',{'cartitems':cartitems,'customeraddresses':customeraddresses,'totalprice':totalprice(request),'totalitems':totalitems(request),'order':order})

def singleordersummary(request,product_pk):
    
    product=get_object_or_404(Product,pk=product_pk)
    customeraddresses=CustomerAddress.objects.filter(customer=request.user)
    # Size price
    productprice=0
    amount=0
    if request.POST['productsize']=="XS":
        productprice=float(product.XSprice)
    elif request.POST['productsize']=="S":
        productprice=float(product.Sprice)
    elif request.POST['productsize']=="M":
        productprice=float(product.Mprice)
    elif request.POST['productsize']=="L":
        productprice=float(product.Lprice)
    elif request.POST['productsize']=="XL":
        productprice=float(product.XLprice)
    elif request.POST['productsize']=="XXL":
        productprice=float(product.XXLprice)
    elif request.POST['productsize']=="XXXL":
        productprice=float(product.XXXLprice)
    # amount is productprice + shipping price
    amount=productprice+100
    customer=get_object_or_404(Customer,user=request.user)
  
    client = razorpay.Client(auth=("rzp_test_5T9IAkXd2Zeh6q", "4jtzAZkCev9udXHdA99mlcNj"))
    data={
        "amount" : amount*100,
        "currency" : 'INR',
        "receipt" : 'receipt55',
        "notes" : {        
                    # 'name':customer.firstname+" "+customer.lastname,           
                    'email': customer.user.email,
                    'phone':customer.phoneno,                    
                  } 
    }
    # We create an order with the data.
    order=client.order.create(data=data) 
    #Order is an object. We pass this as dictionary    

    return render(request,'customer/ordersummary.html',{'product':product,'customeraddresses':customeraddresses,'singleitem':True,'order':order,'productsize':request.POST['productsize'],'productprice':productprice})

def paymentsuccess(request):
    cartitems=Cart.objects.filter(customer=request.user).order_by('-id')
    customer=get_object_or_404(User,email=request.user)
    amount=0
    for product in cartitems:       
        modelproduct=get_object_or_404(Product,pk=product.product.id)
        price=float(product.price*product.save_quantity)
        amount+=price
        Order(customer=customer,customer_firstname=request.POST['orderfirstname'],customer_lastname=request.POST['orderlastname'],product=modelproduct,product_label=modelproduct.label,seller=modelproduct.user,product_size=product.product_size,buy_quantity=product.save_quantity,to_address=request.POST['orderaddress'],order_date=datetime.date.today(),delivery_date=datetime.date.today()+datetime.timedelta(days=5),price=price).save()
        cart=get_object_or_404(Cart,customer=customer,product=modelproduct)
        cart.delete()
        # To reduce product of that size from database when ordered
        if product.product_size=="XS":
            modelproduct.XS-=product.save_quantity
            modelproduct.save()
        elif product.product_size=="S":
            modelproduct.S-=product.save_quantity
            modelproduct.save()
        elif product.product_size=="M":
            modelproduct.M-=product.save_quantity
            modelproduct.save()
        elif product.product_size=="L":
            modelproduct.L-=product.save_quantity
            modelproduct.save()
        elif product.product_size=="XL":
            modelproduct.XL-=product.save_quantity
            modelproduct.save()
        elif product.product_size=="XXL":
            modelproduct.XXL-=product.save_quantity
            modelproduct.save()
        elif product.product_size=="XXXL":
            modelproduct.XXXL-=product.save_quantity
            modelproduct.save()
   
    return render(request,'customer/paymentsuccess.html',{'cartitems':cartitems,'orderfirstname':request.POST['orderfirstname'],'orderlastname':request.POST['orderlastname'],'orderaddress':request.POST['orderaddress'],'totalpaid':amount+100})
   

def singlepaymentsuccess(request):
    customer=get_object_or_404(User,email=request.user)         
    modelproduct=get_object_or_404(Product,pk=request.POST['productid'])
    productprice=float(request.POST['productprice'])
    Order(customer=customer,customer_firstname=request.POST['orderfirstname'],customer_lastname=request.POST['orderlastname'],product=modelproduct,product_label=modelproduct.label,seller=modelproduct.user,product_size=request.POST['productsize'],buy_quantity=1,to_address=request.POST['orderaddress'],order_date=datetime.date.today(),delivery_date=datetime.date.today()+datetime.timedelta(days=5),price=productprice).save()
    # To reduce product of that size from database when ordered
    if request.POST['productsize']=="XS":
        modelproduct.XS-=1
        modelproduct.save()
    elif request.POST['productsize']=="S":
        modelproduct.S-=1
        modelproduct.save()
    elif request.POST['productsize']=="M":
        modelproduct.M-=1
        modelproduct.save()
    elif request.POST['productsize']=="L":
        modelproduct.L-=1
        modelproduct.save()
    elif request.POST['productsize']=="XL":
        modelproduct.XL-=1
        modelproduct.save()
    elif request.POST['productsize']=="XXL":
        modelproduct.XXL-=1
        modelproduct.save()
    elif request.POST['productsize']=="XXXL":
        modelproduct.XXXL-=1
        modelproduct.save()
    return render(request,'customer/paymentsuccess.html',{'singleitem':True,'product':modelproduct,'productprice':productprice,'productsize':request.POST['productsize'],'orderfirstname':request.POST['orderfirstname'],'orderlastname':request.POST['orderlastname'],'orderaddress':request.POST['orderaddress'],'totalpaid':productprice+100})
   