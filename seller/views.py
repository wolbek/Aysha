import datetime
from django.http import HttpResponseRedirect

# from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from user.models import Customer, User,Seller
from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate, update_session_auth_hash
from django.db import IntegrityError
from seller.forms import ProductForm 
from django.contrib import messages
from user.forms import ChangePasswordForm
from seller.models import Product
from customer.models import Order
from customer.forms import OrderForm
from .serializers import ProductSerializer,OrderSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.decorators import api_view
from django.http.response import JsonResponse


# Create your views here.

def signupseller(request):
    if request.method=='GET':
        return render(request,'seller/signupseller.html')
    else:                   
        user=User.objects.create_user(request.POST['email'],request.POST['password1'],is_seller=True)
        Seller.objects.create(user=user,phoneno=request.POST['phoneno'],shopname=request.POST['shopname'],warehouselocation=request.POST['warehouselocation'])
        
        login(request,user)
        return redirect('seller:dashboard')          

@api_view(['GET'])
def emailregistered(request):    
    print("LOL")
    user=User.objects.filter(email=request.GET['email'])
    error=""         
    try:   
        qs_seller=user.values("is_seller")
        is_seller=qs_seller[0]['is_seller']
        qs_customer=user.values("is_customer")
        is_customer=qs_customer[0]['is_customer']

        if is_seller:
            error="Email already registered as Seller"
        elif is_customer:
            error="Email already registered as Customer"
    except:
        error="Not registered"

    return JsonResponse({'error':error})

def dashboard(request):
    products=Product.objects.filter(user=request.user)
    orders=Order.objects.filter(seller=request.user)
    orderpending=Order.objects.filter(seller=request.user,delivered_date__isnull=True)
    ordercompleted=Order.objects.filter(seller=request.user,delivered_date__isnull=False)
    totalprice=0  
    productcount=products.count
    orderpendingcount=orderpending.count()
    ordercompletedcount=ordercompleted.count()
    orderpending=Order.objects.filter(seller=request.user,delivered_date__isnull=True)[:6]
    for i in orders:
        totalprice+=i.price   
    products=Product.objects.filter(user=request.user).order_by('-id')[:8]
    return render(request,'seller/dashboard.html',{'products':products,'orderpending':orderpending,'productcount':productcount,'orderpendingcount':orderpendingcount, 'ordercompletedcount':ordercompletedcount,'totalprice':totalprice})

def loginseller(request):
    if request.method=='GET':
        return render(request,'seller/loginseller.html')
    else:
        seller=authenticate(request,email=request.POST['email'],password=request.POST['password'])

        if seller is None or seller.is_seller==False:
            messages.error(request,'Username and Password did not match')
            return render(request,'seller/loginseller.html')
        else:
            login(request,seller)            
            return redirect('seller:dashboard')
            

def logoutseller(request):
    if request.method=='POST':
        logout(request)
        return redirect('home')

def createproduct(request):
    if request.method=='GET':
        return render(request,'seller/createproduct.html',{'form':ProductForm()})
    else:        
        form=ProductForm(request.POST,request.FILES)
        if form.is_valid():
            newproduct=form.save(commit=False)
            newproduct.user=request.user
            newproduct.save()
            messages.success(request,'Product Created Successfully')
            return redirect('seller:inventory')
        else:
            messages.error(request,form.errors)
            return render(request,'seller/createproduct.html',{'form':ProductForm()})


def changepassword(request):    
    if request.method=='GET':  
        return render(request,'seller/changepassword.html',{'form':ChangePasswordForm(user=request.user)})
    else:
        form=ChangePasswordForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            messages.success(request,'Password changed successfully')
            return HttpResponseRedirect(request.path_info)
        else:
            messages.error(request, form.errors)
            return render(request,'seller/changepassword.html',{'form':ChangePasswordForm(user=request.user),'error':True})

  
def inventory(request):
    products=Product.objects.filter(user=request.user).order_by('-id')
    return render(request,'seller/inventory.html',{'products':products})

def editproduct(request,product_pk):    
    product=get_object_or_404(Product,pk=product_pk,user=request.user)  
    if request.method=='GET':             
        return render(request,'seller/editproduct.html',{'product':product,'form':ProductForm(instance=product)})
    else:
        form=ProductForm(request.POST,request.FILES,instance=product)
        if form.is_valid():                  
            form.save()
            messages.success(request,'Product Edited Succuessfully')
            return redirect('seller:inventory')
        else:
            messages.error(request,form.errors)
            return render(request,'seller/editproduct.html',{'product':product,'form':ProductForm(instance=product)})

def deleteproduct(request):
    product=get_object_or_404(Product,pk=request.POST['pid'],user=request.user) 
    if request.method=="POST":
        product.delete()       
        return JsonResponse({'status':1})

#Respond when search button is clicked in inventory.html
@api_view(['GET'])
def productlist(request):
    products=Product.objects.filter(label__icontains=request.GET['searchcontent'],user=request.user).order_by('-id')
    serializer=ProductSerializer(products,many=True) 
    return Response(serializer.data)

def orderpending(request):
    if request.method=='GET':
        orders=Order.objects.filter(seller=request.user,delivered_date__isnull=True).order_by('-id')
        return render(request,"seller/orderpending.html",{'orders':orders})
    else:
        order=get_object_or_404(Order,pk=request.POST['oid'])
        order.delivery_status=request.POST['delivery_status']
        if order.delivery_status=='Delivered':
            order.delivered_date=timezone.now()
            order.save() 
            return JsonResponse({'status':0})
        else:
            order.save() 
            return JsonResponse({'status':1})      

def ordercompleted(request):
    orders=Order.objects.filter(seller=request.user, delivered_date__isnull=False).order_by('-id')
    return render(request,"seller/ordercompleted.html",{'orders':orders})

#Respond when search button is clicked in orderpending.html
@api_view(['GET'])
def orderlist(request):
    orders=Order.objects.filter(product_label__icontains=request.GET['searchcontent'],delivered_date__isnull=True,seller=request.user).order_by('-id')
    serializer=OrderSerializer(orders,many=True)
    return Response(serializer.data)

#Respond when search button is clicked in ordercompleted.html
@api_view(['GET'])
def completedorderlist(request):
    orders=Order.objects.filter(product_label__icontains=request.GET['searchcontent'],delivered_date__isnull=False,seller=request.user).order_by('-id')
    serializer=OrderSerializer(orders,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def genderchart(request):
   
    malecount=Customer.objects.filter(gender="M").count()
    print(malecount)
    femalecount=Customer.objects.filter(gender="F").count()
    
    data={
        "labels":["male","female"],
        "items":[malecount,femalecount]       
    }
    return Response(data)

# Respond when analytic.html is opened and also when selected product or selected option is changed
@api_view(['GET'])
def productdata(request):
    labels=[]
    items=[]
    
    if request.GET['timeoption']=="Last 7 days":
        d=datetime.date.today()
        for i in range(6,-1,-1):
            labels.append(d-datetime.timedelta(days=i))    
          
    elif request.GET['timeoption']=="Last 28 days":
        d=datetime.date.today()
        for i in range(27,-1,-1):
            labels.append(d-datetime.timedelta(days=i))   
        

    elif request.GET['timeoption']=="Last 90 days":
        d=datetime.date.today()
        for i in range(89,-1,-1):
            labels.append(d-datetime.timedelta(days=i))
    

    if request.GET['productoption']=='all':
        for i in labels:
            productordercount=Order.objects.filter(seller=request.user,order_date=i).count()
            items.append(productordercount)
    else:
        for i in labels:
            productordercount=Order.objects.filter(product=request.GET['productoption'],order_date=i).count()
            items.append(productordercount)
            # print(i) 

    data={
        "labels":labels,
        "items":items,
        "total":sum(items)
    }
   
    return Response(data)

def analytic(request):
    products=Product.objects.filter(user=request.user)
    orders=Order.objects.filter(seller=request.user)
    totalprice=0  
    for i in orders:
        totalprice+=i.price   
    return render(request,'seller/analytic.html',{'products':products,'totalprice':totalprice})


