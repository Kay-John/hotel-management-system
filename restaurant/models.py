from django.db import models

class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('APPETIZER', 'Appetizer'),
        ('LOCAL_DISHES', 'Local Dishes'),
        ('SNACKS', 'Snacks'),
        ('DESSERT', 'Dessert'),
        ('THE_BAR', 'The Bar'),
        ('COFFEE_AND_TEAS', 'Coffee and Teas'),
        ('SOFT_DRINKS', 'Soft drinks'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='menu_items/', null=True, blank=True)
    daily_opening_stock = models.PositiveIntegerField(default=0)
    current_stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Table(models.Model):
    table_number = models.CharField(max_length=10, unique=True)
    capacity = models.PositiveIntegerField()
    qr_code = models.ImageField(upload_to='table_qr_codes/', null=True, blank=True)

    def save(self, *args, **kwargs):
        from .utils import generate_qr_code
        url = f"https://jk-hotel-management-system.onrender.com/menu/?table={self.table_number}"
        self.qr_code = generate_qr_code(url)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Table {self.table_number}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SERVED', 'Served'),
        ('PAID', 'Paid'),
        ('CANCELLED', 'Cancelled'),
    ]

    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='orders')
    items = models.ManyToManyField(MenuItem, through='OrderItem', related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    charge_to_room = models.ForeignKey(
        'hotel.Stay',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='restaurant_orders',
        help_text="Link to guest stay for room folio charging"
    )

    def apply_charge_to_room(self):
        """Appends the restaurant order total to the guest's final hotel bill."""
        if self.charge_to_room:
            self.charge_to_room.total_room_charge += self.total_amount
            self.charge_to_room.save()
            return True
        return False

    def __str__(self):
        return f"Order {self.id} - Table {self.table.table_number}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if is_new:
            self.item.current_stock -= self.quantity
            self.item.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"
