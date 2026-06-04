from django.test import TestCase
from django.utils import timezone
from .models import Room, Guest, Stay
from decimal import Decimal

class HotelModelTest(TestCase):

    def setUp(self):
        self.room = Room.objects.create(
            number="101",
            room_type="SINGLE",
            price_per_night=Decimal("100.00"),
            status="AVAILABLE"
        )
        self.guest = Guest.objects.create(
            name="John Doe",
            phone="1234567890",
            email="john@example.com"
        )

    def test_room_creation(self):
        self.assertEqual(self.room.number, "101")
        self.assertEqual(str(self.room), "Room 101 (SINGLE)")

    def test_guest_creation(self):
        self.assertEqual(self.guest.name, "John Doe")
        self.assertEqual(str(self.guest), "John Doe")

    def test_stay_creation(self):
        check_in = timezone.now()
        stay = Stay.objects.create(
            guest=self.guest,
            room=self.room,
            check_in=check_in,
            total_room_charge=Decimal("200.00"),
            is_active=True
        )
        self.assertEqual(stay.guest, self.guest)
        self.assertEqual(stay.room, self.room)
        self.assertEqual(stay.total_room_charge, Decimal("200.00"))
        self.assertTrue(stay.is_active)
        self.assertEqual(str(stay), "Stay: John Doe in 101")
