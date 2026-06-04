from django.contrib import admin
from .models import MenuItem, Table, Order

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    list_filter = ('category',)
    search_fields = ('name',)

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'capacity')
    search_fields = ('table_number',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'table', 'total_amount', 'status', 'charge_to_room')
    list_filter = ('status', 'table')
    search_fields = ('table__table_number', 'charge_to_room__guest__name')
    filter_horizontal = ('items',)
