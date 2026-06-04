from django.test import TestCase
from .models import MenuItem, Table, Order
from hotel.models import Room, Guest, Stay
from decimal import Decimal
from django.utils import timezone

class RestaurantModelTest(TestCase):

    def setUp(self):
        self.menu_item = MenuItem.objects.create(
            name="Burger",
            category="MAIN_COURSE",
            price=Decimal("15.00")
        )
        self.table = Table.objects.create(
            table_number="A1",
            capacity=4
        )
        self.room = Room.objects.create(
            number="101",
            room_type="SINGLE",
            price_per_night=Decimal("100.00")
        )
        self.guest = Guest.objects.create(
            name="Jane Doe",
            phone="9876543210",
            email="jane@example.com"
        )
        self.stay = Stay.objects.create(
            guest=self.guest,
            room=self.room,
            check_in=timezone.now(),
            total_room_charge=Decimal("0.00")
        )

    def test_menu_item_creation(self):
        self.assertEqual(self.menu_item.name, "Burger")
        self.assertEqual(str(self.menu_item), "Burger")

    def test_table_creation(self):
        self.assertEqual(self.table.table_number, "A1")
        self.assertEqual(str(self.table), "Table A1")

    def test_order_creation(self):
        order = Order.objects.create(
            table=self.table,
            total_amount=Decimal("15.00"),
            status="PENDING"
        )
        order.items.add(self.menu_item)
        self.assertEqual(order.table, self.table)
        self.assertIn(self.menu_item, order.items.all())
        self.assertEqual(order.total_amount, Decimal("15.00"))
        self.assertEqual(order.status, "PENDING")

    def test_order_with_folio_charging(self):
        order = Order.objects.create(
            table=self.table,
            total_amount=Decimal("15.00"),
            status="PAID",
            charge_to_room=self.stay
        )
        self.assertEqual(order.charge_to_room, self.stay)
        self.assertEqual(self.stay.restaurant_orders.first(), order)

    def test_apply_charge_to_room(self):
        order = Order.objects.create(
            table=self.table,
            total_amount=Decimal("25.50"),
            status="PAID",
            charge_to_room=self.stay
        )
        success = order.apply_charge_to_room()
        self.assertTrue(success)
        self.stay.refresh_from_db()
        self.assertEqual(self.stay.total_room_charge, Decimal("25.50"))

    def test_apply_charge_to_room_no_stay(self):
        order = Order.objects.create(
            table=self.table,
            total_amount=Decimal("10.00"),
            status="PAID"
        )
        success = order.apply_charge_to_room()
        self.assertFalse(success)
