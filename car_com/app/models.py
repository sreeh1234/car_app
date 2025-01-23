from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import CharField
from django.utils.translation import gettext_lazy as _
from .constants import PaymentStatus

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


class Order(models.Model):
    name = CharField(_("Customer Name"), max_length=254, blank=False, null=False)
    amount = models.FloatField(_("Amount"), null=False, blank=False)
    status = CharField(
        _("Payment Status"),
        default=PaymentStatus.PENDING,
        max_length=254,
        blank=False,
        null=False,
    )
    provider_order_id = models.CharField(
        _("Order ID"), max_length=40, null=False, blank=False
    )
    payment_id = models.CharField(
        _("Payment ID"), max_length=36, null=False, blank=False
    )
    signature_id = models.CharField(
        _("Signature ID"), max_length=128, null=False, blank=False
    )

    def __str__(self):
        return f"{self.id}-{self.name}-{self.status}"