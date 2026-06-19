from django.test import TestCase
from django.utils import timezone
from .models import Room, Guest, Stay

class HotelModelTest(TestCase):
    def setUp(self):
        self.room = Room.objects.create(number="101", room_type="SINGLE", price_per_night=100.00)
        self.guest = Guest.objects.create(name="John Doe", phone="123456789", email="john@example.com")

    def test_room_creation(self):
        self.assertEqual(self.room.status, 'AVAILABLE')
        self.assertEqual(str(self.room), "Room 101 (SINGLE)")

    def test_stay_creation(self):
        stay = Stay.objects.create(
            guest=self.guest,
            room=self.room,
            check_in=timezone.now(),
            total_room_charge=100.00
        )
        self.assertEqual(stay.guest.name, "John Doe")
        self.assertTrue(stay.is_active)
