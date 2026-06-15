import os
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from .models import MenuItem

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
