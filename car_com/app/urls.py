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
    path('view_products/<id>',views.view_products),
    path('delete_category/<id>',views.delete_category),
    path('detail',views.detail),
    path('bookings',views.bookings),
    


    
    
    
    path('register',views.register),
    path('otp',views.otp_confirmation),
    path('user_home',views.user_home),
    path('view_product/<pid>',views.viewpro),
    path('addtocart/<pid>',views.add_to_cart),
    path('viewcart',views.view_cart),
    path('increment/<cid>',views.qty_incri),
    path('decrement/<cid>',views.qty_dec),
    path('buyproduct/<pid>/<address>',views.buy_product,name="buyproduct"),
    path('userbookings',views.user_bookings),
    
    path('buyNow/<pid>',views.buyNow),
    path('orderSummary/<Products>/<data>',views.orderSummary,name="orderSummary"),
    path('orderSummary2/<price>/<total>',views.orderSummary2,name="orderSummary2"),
    path('address',views.address),
    path('delete_address/<pid>',views.delete_address),
    path('cart_buy',views.cart_buy),
    path('order_payment/<pid>/<address>',views.order_payment,name="payment"),
    

]