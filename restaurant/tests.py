from django.test import TestCase, override_settings
from .models import MenuItem, Order, Table
from unittest.mock import patch
from django.core.files import File
from io import BytesIO

@override_settings(STORAGES={
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
})
class RestaurantModelTest(TestCase):
    def setUp(self):
        self.item = MenuItem.objects.create(name="Test Item", price=10.00, current_stock=5)
        # Mock generate_qr_code in utils to avoid Cloudinary/file system issues
        with patch('restaurant.utils.generate_qr_code') as mocked_qr:
            mocked_qr.return_value = File(BytesIO(b"fake_qr"), name='test_qr.png')
            self.table = Table.objects.create(table_number="1", capacity=4)

    def test_order_creation(self):
        order = Order.objects.create(order_type='DINE_IN', table=self.table)
        self.assertEqual(order.status, 'PENDING')
        self.assertEqual(order.order_type, 'DINE_IN')

    def test_order_type_choices(self):
        order = Order.objects.create(order_type='TAKEAWAY')
        self.assertIsNone(order.table)
        self.assertEqual(order.order_type, 'TAKEAWAY')
