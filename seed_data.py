import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_management_system.settings')
django.setup()

from django.conf import settings
from restaurant.models import MenuItem, Table, Order, OrderItem

# Temporarily disable Cloudinary for seeding if keys are missing
if not os.environ.get('CLOUDINARY_API_KEY'):
    settings.STORAGES['default']['BACKEND'] = 'django.core.files.storage.FileSystemStorage'

# Create Tables
for i in range(1, 6):
    Table.objects.get_or_create(table_number=f"A{i}", defaults={'capacity': 4})
for i in range(1, 6):
    Table.objects.get_or_create(table_number=f"B{i}", defaults={'capacity': 2})

# Create Menu Items
items = [
    ('Scrambled Eggs With Toast', 'APPETIZER', 15000),
    ('Tacos With Chicken Grilled', 'SNACKS', 25000),
    ('Spaghetti Bolognese', 'LOCAL_DISHES', 35000),
    ('French Bread & Potato', 'APPETIZER', 12000),
    ('Chicken Biriyani', 'LOCAL_DISHES', 40000),
    ('Hawaiian Chicken Skewers', 'SNACKS', 28000),
]

for name, cat, price in items:
    MenuItem.objects.get_or_create(name=name, defaults={'category': cat, 'price': price, 'current_stock': 10, 'daily_opening_stock': 10})

# Create some orders
t1 = Table.objects.get(table_number='A4')
t2 = Table.objects.get(table_number='B2')
m1 = MenuItem.objects.get(name='Scrambled Eggs With Toast')

o1, _ = Order.objects.get_or_create(table=t1, status='SERVED', defaults={'total_amount': 15000})
OrderItem.objects.get_or_create(order=o1, item=m1, defaults={'quantity': 1})

o2, _ = Order.objects.get_or_create(table=t2, status='PENDING', defaults={'total_amount': 30000})
OrderItem.objects.get_or_create(order=o2, item=m1, defaults={'quantity': 2})
