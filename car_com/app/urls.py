from django .urls import path 
from . import views 


urlpatterns=[
     path('',views.user_login),
    path('shop_home',views.shop_home),
    path('logout',views.user_logout),
    
    
    
    
    
     path('register',views.register),
     path('user_home',views.user_home),
]