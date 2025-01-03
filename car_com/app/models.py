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
    product=models.ForeignKey(product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    qty=models.IntegerField()    