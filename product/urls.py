# urls.py
from django.urls import path
from .views import home, purchase_product, manage_inventory, add_product_page, product_list, add_product
from product import views

urlpatterns = [
    #Authentication
    path('signup/' ,views.SignupPage,name='signup' ),
    path('login' ,views.login,name='login' ),
    path('' ,views.LoginPage,name='loginpage' ),
    path('loginpage/' ,views.LoginPage,name='loginpage' ),
    path('register' ,views.RegisterPage,name='register' ),

    #Seller
    path('manage_inventory/<int:product_id>/', manage_inventory, name='manage_inventory'),
    path('add_product_page/', add_product_page, name='add_product_page'),
    path('add_product', add_product, name='add_product'),

    #Customer
    path('home/', home, name='home'),
    path('purchase/<int:product_id>/', purchase_product, name='purchase_product'),
    path('product_list/', product_list, name='product_list')
]
