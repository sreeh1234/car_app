from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
import os
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
import random

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
        price = req.POST['price']
        offer_price = req.POST['offer_price']
        stock = req.POST['stock']
        weight = req.POST['weight']
        img=req.FILES.get('img')
        pro_data=product.objects.get(pk=id)
        if img:
            product.objects.filter(pk=id).update(pid=pid,name=name,dis=dis)
            data=product.objects.get(pk=id)
            data.img=img
            data.save()
        else:
             product.objects.filter(pk=id).update(pid=pid,name=name,dis=dis)
        # return redirect(shop_home)  

        details.objects.filter(product=pro_data).update(price=price, offer_price=offer_price, stock=stock,weight=weight)
        return redirect(shop_home)   
    else:
        pro_data=product.objects.get(pk=id)
        Details = details.objects.get(product=pro_data)       
        return render(req,'shop/edit.html',{'pro_data':pro_data,'Details':Details}) 
    

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
    if req.method=='POST':
        uname=req.POST['uname']
        email=req.POST['email']
        pswd=req.POST['pswd']
        try:
            data=User.objects.create_user(first_name=uname,email=email,username=email,password=pswd)
            data.save()
            otp=""
            for i in range(6):
                otp+=str(random.randint(0,9))
            msg=f'Your registration is completed otp: {otp}'
            otp=Otp.objects.create(user=data,otp=otp)
            otp.save()
            send_mail('Registration',msg, settings.EMAIL_HOST_USER, [email])
            return redirect(otp_confirmation)
        except:
            messages.warning(req,'Email already exist')
            return redirect(register)
    else:
        return render(req,'user/register.html')


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
        return render(req,'user/home.html',{'product':products})
    else:
        return redirect(car_com_login)
    
def viewpro(req,pid):
    data=product.objects.get(pk=pid) 
    Detail=details.objects.filter(product=pid)
    Detail2=details.objects.get(product=pid,pk=Detail[0].pk)
    if req.GET.get('dis'):
            dis=req.GET.get('dis')
            Detail2=details.objects.get(product=pid,pk=dis)
    return render(req,'user/view.html',{'data':data,'Detail':Detail,'Detail2':Detail2})    


def add_to_cart(req,pid):
    detail=details.objects.get(pk=pid) 
    user=User.objects.get(username=req.session['user'])
    try:
        Cart=cart.objects.get(details=detail,user=user)
        Cart.qty+=1
        Cart.save()
    except:    
        data=cart.objects.create(details=detail,user=user,qty=1)
        data.save()
    return redirect(view_cart)

def view_cart(req):
    user=User.objects.get(username=req.session['user'])
    data=cart.objects.filter(user=user)
    return render(req,'user/cart.html',{'cart':data})

def qty_incri(req,cid):
    data=cart.objects.get(pk=cid)
    print(data.qty)
    print(data.details.stock)
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



def buy_product(req,pid):
    detail=details.objects.get(pk=pid)
    user=User.objects.get(username=req.session['user'])
    qty=1
    price=detail.offer_price
    buy=Buy.objects.create(details=detail,user=user,qty=qty,t_price=price)
    buy.save()
    return redirect(user_bookings)


def cart_buy(req,cid):

    Cart=cart.objects.get(pk=cid)
    price=Cart.qty*Cart.details.offer_price
    stock=Cart.details.stock-Cart.qty
    if stock==0:
        messages.warning(req,'OUT OF STOCK'+Cart.details.product.name)
        return redirect(view_cart)
    buy=Buy.objects.create(details=Cart.details,user=Cart.user,qty=Cart.qty,t_price=price)
    buy.save()
    return redirect(user_bookings)   


    

def user_bookings(req):
    user=User.objects.get(username=req.session['user'])
    bookings=Buy.objects.filter(user=user)[::-1]
    return render(req,'user/bookings.html',{'bookings':bookings})