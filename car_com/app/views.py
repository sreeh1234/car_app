from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
import os
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
import random
import razorpay
import json
from django.views.decorators.csrf import csrf_exempt


# Create your views here.


def car_com_login(req):
    if 'shop' in req.session:
        return redirect(shop_home)
    if 'user' in req.session:
        return redirect(user_home)
    if req.method=='POST':
        uname=req.POST['uname']
        password=req.POST['password']
        shop=authenticate(username=uname,password=password)
        if shop:
            login(req,shop)
            if shop.is_superuser:
                
                req.session['shop']=uname       #create
                return redirect(shop_home)
            else:
                req.session['user']=uname
                return redirect(user_home)
        else:
            messages.warning(req,'invalid username or password')
            return redirect(car_com_login)
    else:
        return render(req,'login.html')

def car_com_logout(req):
    logout(req)
    req.session.flush()        
    return redirect(car_com_login)

# --------------------------------SHOP--------------------------------------
# --------------------------------------------------------------------------




def shop_home(req):
    if 'shop' in req.session:
        products=details.objects.all()
        return render(req,'shop/home.html',{'product':products})
    else:
        return redirect(car_com_login)


def addpro(req):
    if 'shop' in req.session:
        if req.method=='POST':
            pid=req.POST['pid']
            name=req.POST['name']
            dis=req.POST['dis']
            categories=req.POST['cat']
            img=req.FILES.get('img')
            data=product.objects.create(pid=pid,name=name,dis=dis,categories=category.objects.get(categories=categories),img=img)
            data.save()
            return redirect(detail)
        else:
            data=category.objects.all()
            return render(req,'shop/addpro.html',{'data':data})  
    else:
        return redirect(car_com_login) 
    
def cat(req):
    if req.method=="POST":
        categories=req.POST['category']
        data=category.objects.create(categories=categories)
        data.save()
        return redirect(cat)
    else:
        data=category.objects.all()
        return render(req,'shop/category.html',{'data':data}) 

def view_products(req,id):
    category1 = category.objects.get(pk=id)
    detail = details.objects.filter(product__categories=category1)
    return render(req, 'shop/viewproducts.html', {'category': category1,'detail': detail})

def delete_category(req,id):
    data=category.objects.get(pk=id)
    data.delete()
    return redirect(cat)


def detail(req):
    if req.method=='POST':
        pro=req.POST['pid']
        price=req.POST['price']
        offer_price=req.POST['offer_price']
        stock=req.POST['stock']
        weight=req.POST['weight']
        data=details.objects.create(price=price,offer_price=offer_price,stock=stock,weight=weight,product=product.objects.get(pk=pro))
        data.save()
        return redirect(shop_home)
    else:
        data=product.objects.all()
        return render(req,'shop/details.html',{'data':data})    


def editpro(req,id):
    if req.method=='POST':
        pid=req.POST['pid']
        name=req.POST['name']
        dis=req.POST['dis']
        img=req.FILES.get('img')
        if img:
            product.objects.filter(pk=id).update(pid=pid,name=name,dis=dis)
            data=product.objects.get(pk=id)
            data.img=img
            data.save()
        else:
            product.objects.filter(pk=id).update(pid=pid,name=name,dis=dis)
        return redirect(shop_home)
    else:
        data=product.objects.get(pk=id)      
        return render(req,'shop/editpro.html',{'data':data})
    
def editdetails(req,pid):
    if req.method == 'POST':
        Details = req.POST['d_id']
        # print(Details)
        # pro=req.POST['pid']
        weight=req.POST['weight']
        price=req.POST['price']
        offer_price=req.POST['offer_price']
        stock=req.POST['stock']
        details.objects.filter(pk=Details).update(product=product.objects.get(pk=pid),weight=weight,price=price,offer_price=offer_price,stock=stock)
        return redirect(shop_home)
    else:      
        data=details.objects.filter(product=pid)
        data1=product.objects.get(pk=pid)
        return render(req,'shop/editdet.html',{'data':data,'data1':data1})    


def bookings(req):
    booking=Buy.objects.all()[::-1]
    return render(req,'shop/bookings.html',{'bookings':booking})

def delete(req,pid):
    data=product.objects.get(pk=pid)
    file=data.img.url
    file=file.split('/')[-1]
    os.remove('media/'+file)
    data.delete()
    return redirect(shop_home)
   





# -----------------------------------user----------------------------------------
# -------------------------------------------------------------------------------


def register(req):
    if req.method == 'POST':
        uname = req.POST['uname']
        email = req.POST['email']
        pswd = req.POST['pswd']
        try:
            data = User.objects.create_user(first_name=uname, email=email, username=email, password=pswd)
            data.save()
            otp = ""
            for i in range(6):
                otp += str(random.randint(0, 9))
            msg = f'Your registration is completed otp: {otp}'
            otp = Otp.objects.create(user=data, otp=otp)
            otp.save()
            send_mail('Registration', msg, settings.EMAIL_HOST_USER, [email])
            messages.success(req, "Registration successful. Please check your email for OTP.")
            return redirect(otp_confirmation)
        except:
            messages.warning(req, 'Email already exists')
            return redirect(register)
    else:
        return render(req, 'user/register.html')

    
def otp_confirmation(req):
    if req.method == 'POST':
        uname = req.POST.get('uname')
        user_otp = req.POST.get('otp')
        try:
            user = User.objects.get(username=uname)
            generated_otp = Otp.objects.get(user=user)
    
            if generated_otp.otp == user_otp:
                generated_otp.delete()
                return redirect(car_com_login)
            else:
                messages.warning(req, 'Invalid OTP')
                return redirect(otp_confirmation)
        except User.DoesNotExist:
            messages.warning(req, 'User does not exist')
            return redirect(otp_confirmation)
        except Otp.DoesNotExist:
            messages.warning(req, 'OTP not found or expired')
            return redirect(otp_confirmation)
    return render(req, 'user/otp.html')

def user_home(req):
    if 'user' in req.session:
        products=product.objects.all()
        data=category.objects.all()
        return render(req,'user/home.html',{'product':products,'data':data})
    else:
        return redirect(car_com_login)

def dummy_home(req):
    if 'user' in req.session:
        return redirect(user_home) 
    if 'shop' in req.session:
        return redirect(shop_home)
        
    products=product.objects.all()
    data=category.objects.all()
    return render(req,'user/dummyhome.html',{'product':products,'data':data})
        
    

    
def viewpro(req,pid):
    if 'user' in req.session:
        data=product.objects.get(pk=pid) 
        Detail=details.objects.filter(product=pid)
        Detail2=details.objects.get(product=pid,pk=Detail[0].pk)
        categories=category.objects.all()
        if req.GET.get('dis'):
                dis=req.GET.get('dis')
                Detail2=details.objects.get(product=pid,pk=dis)
        return render(req,'user/view.html',{'data':data,'Detail':Detail,'Detail2':Detail2,'categories':categories})
    else:
        return redirect(car_com_login)    


def add_to_cart(req,pid):
    detail=details.objects.get(pk=pid) 
    user=User.objects.get(username=req.session['user'])
    try:
        Cart=cart.objects.get(details=detail,user=user)
        Cart.qty+=1
        Cart.save()
    except:    
        if detail.stock>0:
            data=cart.objects.create(details=detail,user=user,qty=1)
            data.save()
            detail.stock-=1
            detail.save()
    if detail.stock>0:
        detail.stock-=1
        detail.save()        
    return redirect(view_cart)

def view_product(req,id):
    if 'user' in req.session:
        category1 = category.objects.get(pk=id)
        detail = details.objects.filter(product__categories=category1)
        return render(req, 'user/viewproduct.html', {'category': category1,'detail': detail})
    else:
         return redirect(car_com_login)


def view_cart(req):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        data=cart.objects.filter(user=user)
        return render(req,'user/cart.html',{'cart':data})
    else:
        return redirect(car_com_login)

def qty_incri(req,cid):
    data=cart.objects.get(pk=cid)
    # print(data.qty)
    # print(data.details.stock)
    if data.details.stock > data.qty:
        data.qty+=1
        data.save()
    return redirect(view_cart)   


def qty_dec(req,cid):
    data=cart.objects.get(pk=cid)
    data.qty-=1
    data.save()
    if data.qty==0:
        data.delete()
    return redirect(view_cart)   

def buyNow(req,pid):
    if 'user' in req.session:
        Products=details.objects.get(pk=pid)
        user=User.objects.get(username=req.session['user'])
        data=Address.objects.filter(user=user)
        if data:
            return redirect("orderSummary",Products=Products.pk,data=data)
        else:
            if req.method=='POST':
                user=User.objects.get(username=req.session['user'])
                name=req.POST['name']
                phn=req.POST['phn']
                house=req.POST['house']
                street=req.POST['street']
                pin=req.POST['pin']
                state=req.POST['state']
                data=Address.objects.create(user=user,name=name,phn=phn,house=house,street=street,pin=pin,state=state)
                data.save()
                return redirect("orderSummary",Products=Products.pk,data=data)
            else:
                return render(req,"user/addaddress.html")
    else:
        return redirect(car_com_login) 

   
def cart_buy(req):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        Cart=cart.objects.filter(user=user)
        price=0
        for i in Cart:
            price+=(i.details.offer_price)*i.qty
            # cost+=(i.details.price)-(total)*i.qty
            total=price
            data=Address.objects.filter(user=user)
        if data:
            return redirect("orderSummary2",price=price,total=total)
        else:
            if req.method=='POST':
                user=User.objects.get(username=req.session['user'])
                name=req.POST['name']
                phn=req.POST['phn']
                house=req.POST['house']
                street=req.POST['street']
                pin=req.POST['pin']
                state=req.POST['state']
                data=Address.objects.create(user=user,name=name,phn=phn,house=house,street=street,pin=pin,state=state)
                data.save()
                return redirect("orderSummary2",price=price,total=total)
            else:
                return render(req,"user/addaddress.html")
    else:
        return redirect(car_com_login) 
    
def orderSummary2(req,price,total):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        data=Address.objects.filter(user=user)
        Cart=cart.objects.filter(user=user)
        categories=category.objects.all()
        if req.method == 'POST':
            address=req.POST['address']
            pay=req.POST['pay']
            addr=Address.objects.get(user=user,pk=address)
        else:
            return render(req,'user/orderSummary2.html',{'Cart':Cart,'data':data,'price':price,'total':total,'categories':categories})
        req.session['address']=addr.pk
        if pay == 'paynow':

                return redirect("orderpayment2")    
        else:
                return redirect("buyproduct")    
    else:
        return redirect(car_com_login)
      

def user_bookings(req):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        bookings=Buy.objects.filter(user=user)[::-1]
        return render(req,'user/bookings.html',{'bookings':bookings})
    else:
        return redirect(car_com_login)


def orderSummary(req,Products,data):
    if 'user' in req.session:
        Products=details.objects.get(pk=Products)
        user=User.objects.get(username=req.session['user'])
        data=Address.objects.filter(user=user)
        if req.method == 'POST':
            address=req.POST['address']
            pay=req.POST['pay']
            addr=Address.objects.get(user=user,pk=address)
            print(pay)
        else:
            categories=category.objects.all()
            return render(req,'user/ordersummary.html',{'Products':Products,'data':data,'categories':categories})
        print(Products.pk)
        req.session['address']=addr.pk
        req.session['details']=Products.pk
        if pay == 'paynow':

                return redirect("orderpayment")    
        else:
                return redirect("buyproduct")    
    else:
        return redirect(car_com_login)
    
def order_payment(req):
    if 'user' in req.session:
        user = User.objects.get(username=req.session['user'])
        name = user.first_name
        data=details.objects.get(pk=req.session['details'])
        amount = data.offer_price
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        razorpay_order = client.order.create(
            {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
        )
        order_id=razorpay_order['id']
        order = Order.objects.create(
            name=name, amount=amount, provider_order_id=order_id
        )
        order.save()
        return render(
            req,
            "user/payment.html",
            {
                "callback_url": "http://127.0.0.1:8000/callback",
                "razorpay_key": settings.RAZORPAY_KEY_ID,
                "order": order,
            },
        )
    else:
        return render(car_com_login)

@csrf_exempt
def callback(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id
        order.save()
        if not verify_signature(request.POST):
            order.status = PaymentStatus.SUCCESS
            order.save()
            return render(request, "callback.html", context={"status": order.status})  
        else:
            order.status = PaymentStatus.FAILURE
            order.save()
            return redirect("buyproduct")

    else:
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.status = PaymentStatus.FAILURE
        order.save()
        return render(request, "callback.html", context={"status": order.status})  


def order_payment2(req):
    if 'user' in req.session:
        user = User.objects.get(username=req.session['user'])
        name = user.first_name
        data=cart.objects.filter(user=user)
        amount = 0
        for i in data:
            amount+=(i.details.offer_price)*i.qty
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        razorpay_order = client.order.create(
            {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
        )
        order_id=razorpay_order['id']
        order = Order.objects.create(
            name=name, amount=amount, provider_order_id=order_id
        )
        order.save()
        return render(
            req,
            "user/payment.html",
            {
                "callback_url": "http://127.0.0.1:8000/callback",
                "razorpay_key": settings.RAZORPAY_KEY_ID,
                "order": order,
            },
        )
    else:
        return render(car_com_login)

@csrf_exempt
def callback2(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id
        order.save()
        if not verify_signature(request.POST):
            order.status = PaymentStatus.SUCCESS
            order.save()
            return render(request, "callback.html", context={"status": order.status})  
        else:
            order.status = PaymentStatus.FAILURE
            order.save()
            return redirect("buyproduct")

    else:
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.status = PaymentStatus.FAILURE
        order.save()
        return render(request, "callback.html", context={"status": order.status}) 

def address(req):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        data=Address.objects.filter(user=user)
        if req.method=='POST':
            user=User.objects.get(username=req.session['user'])
            name=req.POST['name']
            phn=req.POST['phn']
            house=req.POST['house']
            street=req.POST['street']
            pin=req.POST['pin']
            state=req.POST['state']
            data=Address.objects.create(user=user,name=name,phn=phn,house=house,street=street,pin=pin,state=state)
            data.save()
            return redirect(address)
        else:
            return render(req,"user/addaddress.html",{'data':data})
    else:
        return redirect(car_com_login) 

def buy_product(req):
    if 'user' in req.session:
        Products=details.objects.get(pk=req.session['details'])
        user=User.objects.get(username=req.session['user'])
        qty=1
        price=Products.offer_price
        buy=Buy.objects.create(details=Products,user=user,qty=qty,t_price=price,Address=Address.objects.get(pk=req.session['address']))
        buy.save()
        Products.stock-=1
        Products.save()
        return redirect(user_bookings)
    else:
        return redirect(car_com_login)    

    
def delete_address(req,pid):
    if 'user' in req.session:
        data=Address.objects.get(pk=pid)
        data.delete()
        return redirect(address)
    else:
        return redirect(car_com_login)    