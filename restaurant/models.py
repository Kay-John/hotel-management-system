from django.db import models

class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('APPETIZER', 'Appetizer'),
        ('MAIN_COURSE', 'Main Course'),
        ('DESSERT', 'Dessert'),
        ('BEVERAGE', 'Beverage'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Table(models.Model):
    table_number = models.CharField(max_length=10, unique=True)
    capacity = models.PositiveIntegerField()

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
    items = models.ManyToManyField(MenuItem, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    stay = models.ForeignKey(
        'hotel.Stay',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='restaurant_orders',
        help_text="Link to guest stay for room folio charging"
    )

    def __str__(self):
        return f"Order {self.id} - Table {self.table.table_number}"
