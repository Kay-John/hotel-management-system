from django.contrib import admin
from .models import Room, Guest, Stay

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'room_type', 'price_per_night', 'status')
    list_filter = ('room_type', 'status')
    search_fields = ('number',)

@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email')
    search_fields = ('name', 'email', 'phone')

@admin.register(Stay)
class StayAdmin(admin.ModelAdmin):
    list_display = ('guest', 'room', 'check_in', 'check_out', 'total_room_charge', 'is_active')
    list_filter = ('is_active', 'check_in')
    search_fields = ('guest__name', 'room__number')
