from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import MenuItem, Table, Order
from .utils import generate_qr_code

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    list_filter = ('category',)
    search_fields = ('name',)

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'capacity', 'qr_code_link')
    search_fields = ('table_number',)
    actions = ['generate_table_qr_codes']

    def generate_table_qr_codes(self, request, queryset):
        for table in queryset:
            menu_url = request.build_absolute_uri(reverse('restaurant:menu'))
            table.qr_code = generate_qr_code(menu_url)
            table.save()
        self.message_user(request, "QR codes generated successfully.")

    generate_table_qr_codes.short_description = "Generate QR codes for selected tables"

    def qr_code_link(self, obj):
        if obj.qr_code:
            return format_html('<a href="{}" download>Download QR</a>', obj.qr_code.url)
        return "No QR Code"

    qr_code_link.short_description = "QR Code"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'table', 'total_amount', 'status', 'charge_to_room')
    list_filter = ('status', 'table')
    search_fields = ('table__table_number', 'charge_to_room__guest__name')
    filter_horizontal = ('items',)
