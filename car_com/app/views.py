from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
import os
from django.contrib.auth.models import User

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
        return redirect(shop_home)
    else:
        data=category.objects.all()
        return render(req,'shop/category.html',{'data':data}) 
    

def detail(req):
    if req.method=='POST':
        pro=req.POST['pid']
        price=req.POST['price']
        offer_price=req.POST['offer_price']
        stock=req.POST['stock']
        weight=req.POST['weight']
        data=details.objects.create(price=price,offer_price=offer_price,stock=stock,weight=weight,product=product.objects.get(pid=pro))
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
        return render(req,'shop/edit.html',{'data':data}) 


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
            return redirect(car_com_login)
        except: 
            messages.warning(req,'Email Already Exist')
            return redirect(register)
    else:
        return render(req,'user/register.html')



def user_home(req):
    if 'user' in req.session:
        products=product.objects.all()
        return render(req,'user/home.html',{'product':products})
    else:
        return redirect(car_com_login)
    
def viewpro(req,pid):
    data=product.objects.get(pk=pid) 
    Detail=details.objects.filter(product=pid)
    return render(req,'user/view.html',{'data':data,'Detail':Detail})    