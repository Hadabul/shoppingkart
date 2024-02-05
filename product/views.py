# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Order, Inventory

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

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
