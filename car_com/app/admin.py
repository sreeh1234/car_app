from django.contrib import admin
from . models import *

# # Register your models here.

admin.site.register(product)
admin.site.register(category)
admin.site.register(details)
admin.site.register(cart)
admin.site.register(Buy)
admin.site.register(Otp)
admin.site.register(Address)