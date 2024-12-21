from django .urls import path 
from . import views 


urlpatterns=[
    path('',views.car_com_login),
    path('shop_home',views.shop_home),
    path('logout',views.car_com_logout),
    path('add product',views.addpro),
    path('edit_product/<id>',views.editpro),
    path('delete_product/<pid>',views.delete),
    path('cat',views.cat),
    path('detail',views.detail),
    
    
    
     path('register',views.register),
     path('user_home',views.user_home),
]