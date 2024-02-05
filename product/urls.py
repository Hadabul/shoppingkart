# urls.py
from django.urls import path
from .views import home, purchase_product, manage_inventory

urlpatterns = [
    path('', home, name='home'),
    path('purchase/<int:product_id>/', purchase_product, name='purchase_product'),
    path('manage_inventory/<int:product_id>/', manage_inventory, name='manage_inventory'),
]
