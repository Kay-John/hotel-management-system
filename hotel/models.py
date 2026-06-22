from django.db import models

class Room(models.Model):
    ROOM_TYPES = [
        ('SINGLE', 'Single'),
        ('DOUBLE', 'Double'),
        ('SUITE', 'Suite'),
    ]
    STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('OCCUPIED', 'Occupied'),
        ('MAINTENANCE', 'Maintenance'),
    ]

    number = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')

    def __str__(self):
        return f"Room {self.number} ({self.room_type})"


class Guest(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Stay(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='stays')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='stays')
    check_in = models.DateTimeField()
    check_out = models.DateTimeField(null=True, blank=True)
    total_room_charge = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Stay: {self.guest.name} in {self.room.number}"
