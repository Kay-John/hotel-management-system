from django.test import TestCase
from django.urls import reverse
from .models import MenuItem, Table, Order, OrderItem
from hotel.models import Room, Guest, Stay
from decimal import Decimal
from django.utils import timezone

class RestaurantModelTest(TestCase):

    def setUp(self):
        self.menu_item = MenuItem.objects.create(
            name="Burger",
            category="LOCAL_DISHES",
            price=Decimal("15.00"),
            daily_opening_stock=10,
            current_stock=10
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

    def test_order_creation_subtracts_stock(self):
        order = Order.objects.create(
            table=self.table,
            total_amount=Decimal("15.00"),
            status="PENDING"
        )
        OrderItem.objects.create(order=order, item=self.menu_item, quantity=2)
        self.menu_item.refresh_from_db()
        self.assertEqual(self.menu_item.current_stock, 8)

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

    def test_menu_view(self):
        response = self.client.get(reverse('restaurant:menu'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Burger")
        self.assertContains(response, "Local Dishes")

    def test_morning_reset_view(self):
        response = self.client.post(reverse('restaurant:morning_reset'), {
            f'stock_{self.menu_item.id}': 50
        })
        self.assertEqual(response.status_code, 302)
        self.menu_item.refresh_from_db()
        self.assertEqual(self.menu_item.daily_opening_stock, 50)
        self.assertEqual(self.menu_item.current_stock, 50)

    def test_eod_report_view(self):
        order = Order.objects.create(table=self.table)
        OrderItem.objects.create(order=order, item=self.menu_item, quantity=3)

        response = self.client.get(reverse('restaurant:eod_report'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Burger")
        self.assertContains(response, "10") # Opening
        self.assertContains(response, "7")  # Current
        self.assertContains(response, "3")  # Sold
        self.assertContains(response, "$45.0") # Expected revenue (3 * 15)
