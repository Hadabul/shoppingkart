# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Order, Inventory, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('confirmPassword')
        role = request.POST.get('role')

        

        if pass1 == pass2:
            # Create a new user
            user = User.objects.create_user(username=uname, email=email, password=pass1)

            # Create a user profile (linked to the user)
            user_profile = UserProfile.objects.create(user=user, username=uname,email=email, password=pass1, role=role )

            # Log in the user after registration
           

            return redirect('home')  # Redirect to the home page or any desired page after registration
        else:
            # Passwords do not match, handle the error (e.g., show an error message in the template)
            pass

    return render(request, 'signup.html')

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def LoginPage(request):
    return render(request, 'login.html')

def login(request):
    if request.method == 'POST':
        uname = request.POST.get('email')
        pass1 = request.POST.get('password')
        response= UserProfile.objects.get(email=uname,)
        print(response)
        if response.password==pass1:
            if response.role=="seller":
                return redirect('product_list')
            else:
                return redirect('home')
    else:
        pass
    return render(request, 'login.html')

def RegisterPage(request):
    return render(request, 'signup.html')

def add_product_page(request):
    return render(request, 'add_product.html')

@login_required
def purchase_product(request, product_id):
    product = Product.objects.get(pk=product_id)
    error_message = ""
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if product.inventory.stock_quantity >= quantity:
            order = Order.objects.create(
                customer=request.user,
                product=product,
                quantity=quantity,
                total_price=quantity * product.price
            )
            product.inventory.stock_quantity -= quantity
            product.inventory.save()
            return redirect('home')
        else:
            error_message = "Insufficient stock quantity."
    return render(request, 'purchase_product.html', {'product': product, 'error_message': error_message})

@login_required
def manage_inventory(request, product_id):
    product = Product.objects.get(pk=product_id)
    if request.method == 'POST':
        new_stock_quantity = int(request.POST.get('stock_quantity'))
        product.inventory.stock_quantity = new_stock_quantity
        product.inventory.save()
    return render(request, 'manage_inventory.html', {'product': product})

def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')

        print(name,description,price,quantity)

        # Create a new product
        product = Product.objects.create(name=name, description=description, price=price)

        # Create an associated inventory entry
        inventory = Inventory.objects.create(product=product, stock_quantity=quantity)

        return redirect('product_list')  # Redirect to a page displaying the product list

    return render(request, 'add_product.html')  # Assuming you have an HTML template for adding products


def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

