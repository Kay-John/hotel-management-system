from django.shortcuts import render
from django.views import View
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

        return render(request, 'restaurant/menu.html', {'grouped_menu': grouped_menu})
