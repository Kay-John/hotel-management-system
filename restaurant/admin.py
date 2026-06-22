from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import MenuItem, Table, Order, OrderItem
from .utils import generate_qr_code

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'daily_opening_stock', 'current_stock', 'image')
    list_filter = ('category',)
    search_fields = ('name',)

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'capacity', 'qr_code_link')
    readonly_fields = ('qr_code_preview',)
    search_fields = ('table_number',)
    actions = ['generate_table_qr_codes']

    def generate_table_qr_codes(self, request, queryset):
        for table in queryset:
            table.save() # Triggers automated QR generation in save()
        self.message_user(request, "QR codes generated successfully.")

    generate_table_qr_codes.short_description = "Generate QR codes for selected tables"

    def qr_code_preview(self, obj):
        if obj.qr_code:
            return format_html(
                '<div style="margin-bottom: 10px;"><img src="{}" style="max-width: 200px; border: 1px solid #ccc;" /></div>'
                '<div><a href="{}" download class="button" style="background: #27ae60; color: white; padding: 5px 10px; text-decoration: none; border-radius: 4px;">Download High-Res PNG</a></div>',
                obj.qr_code.url, obj.qr_code.url
            )
        return "No QR Code generated yet. Save the table to generate one."

    qr_code_preview.short_description = "QR Code Preview"

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
    inlines = [OrderItemInline]
