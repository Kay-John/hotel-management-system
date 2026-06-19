import os
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.db.models import Count, Sum
from .models import MenuItem, Order, Table

class DashboardView(View):
    def get(self, request):
        # New Orders (Pending)
        new_orders = Order.objects.filter(status='PENDING').order_by('-id')
        new_orders_count = new_orders.count()

        # Total Orders
        total_orders_count = Order.objects.count()

        # Active Orders (Pending + Served + Paid) for the processing grid
        # Including PAID so we can show "Completed" status in the list for a while
        active_orders = Order.objects.exclude(status='CANCELLED').order_by('-id')[:20]

        # Payments Pending (Served orders waiting for payment)
        pending_payments = Order.objects.filter(status='SERVED').order_by('-id')

        # Inventory Notifications (Out of stock or low stock < 5)
        out_of_stock_items = MenuItem.objects.filter(current_stock=0)
        low_stock_items = MenuItem.objects.filter(current_stock__gt=0, current_stock__lt=5)

        # Placeholder for Waiting List (In a real system, this might be a separate model)
        waiting_list_count = 0 # Mocking as 0 for now

        # Placeholder for Popular Dishes
        popular_dishes = MenuItem.objects.annotate(order_count=Count('orders')).order_by('-order_count')[:5]

        context = {
            'new_orders_count': new_orders_count,
            'total_orders_count': total_orders_count,
            'waiting_list_count': waiting_list_count,
            'active_orders': active_orders,
            'pending_payments': pending_payments,
            'out_of_stock_items': out_of_stock_items,
            'low_stock_items': low_stock_items,
            'popular_dishes': popular_dishes,
        }
        return render(request, 'dashboard.html', context)

class MenuView(View):
    def get(self, request):
        menu_items = MenuItem.objects.all().order_by('category', 'name')
        grouped_menu = {}
        for item in menu_items:
            category = item.get_category_display()
            if category not in grouped_menu:
                grouped_menu[category] = []
            grouped_menu[category].append(item)

        hotel_name = os.environ.get('HOTEL_NAME', 'Our')
        return render(request, 'restaurant/menu.html', {
            'grouped_menu': grouped_menu,
            'hotel_name': hotel_name
        })


class MorningResetView(View):
    def get(self, request):
        menu_items = MenuItem.objects.all()
        return render(request, 'restaurant/morning_reset.html', {'menu_items': menu_items})

    def post(self, request):
        for key, value in request.POST.items():
            if key.startswith('stock_'):
                item_id = key.split('_')[1]
                stock_value = int(value)
                item = MenuItem.objects.get(id=item_id)
                item.daily_opening_stock = stock_value
                item.current_stock = stock_value
                item.save()
        return redirect('restaurant:morning_reset')


class EODReportView(ListView):
    model = MenuItem
    template_name = 'restaurant/eod_report.html'
    context_object_name = 'menu_items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        report_data = []
        total_expected_revenue = 0

        for item in MenuItem.objects.all():
            portions_sold = item.daily_opening_stock - item.current_stock
            expected_revenue = portions_sold * item.price
            report_data.append({
                'item': item,
                'portions_sold': portions_sold,
                'expected_revenue': expected_revenue
            })
            total_expected_revenue += expected_revenue

        context['report_data'] = report_data
        context['total_expected_revenue'] = total_expected_revenue
        return context
