from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
import os
from django.contrib.auth.models import User

# Create your views here.


def user_login(req):
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
            return redirect(user_login)
    else:
        return render(req,'login.html')

def user_logout(req):
    logout(req)
    req.session.flush()        
    return redirect(user_login)







def shop_home(req):
    # if 'shop' in req.session:
    #     products=product.objects.all()
    return render(req,'shop/home.html')
    # else:
        # return redirect(user_login)




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
            return redirect(user_login)
        except:
            messages.warning(req,'Email Already Exist')
            return redirect(register)
    else:
        return render(req,'user/register.html')



def user_home(req):
    # if 'user' in req.session:
    #     products=product.objects.all()
    return render(req,'user/home.html')
    # else:
    #     return redirect(user_login)