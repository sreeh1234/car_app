from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class category(models.Model):
    categories=models.TextField()

class product(models.Model):
    categories=models.ForeignKey(category,on_delete=models.CASCADE)
    pid=models.TextField(unique=True)
    name=models.TextField()
    dis=models.TextField()
    img=models.FileField()

class details(models.Model):
    product=models.ForeignKey(product,on_delete=models.CASCADE)
    price=models.IntegerField()
    offer_price=models.IntegerField()
    stock=models.IntegerField()    
    weight=models.TextField()

class cart(models.Model):
    details=models.ForeignKey(details,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    qty=models.IntegerField()    

class Address(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.TextField()
    phn=models.IntegerField()
    house=models.TextField()
    street=models.TextField()
    pin=models.IntegerField()
    state=models.TextField()          


class Buy(models.Model):
    Address=models.ForeignKey(Address,on_delete=models.CASCADE)
    details=models.ForeignKey(details,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    qty=models.IntegerField()
    t_price=models.IntegerField()
    date=models.DateField(auto_now_add=True)

class Otp(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    otp=models.TextField()  

