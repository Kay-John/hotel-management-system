import os
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from restaurant.views import MenuView, DashboardView

hotel_name = os.environ.get('HOTEL_NAME', 'Hotel Management System')
admin.site.site_header = hotel_name
admin.site.site_title = hotel_name
admin.site.index_title = hotel_name

urlpatterns = [
    path("admin/", admin.site.urls),
    path("restaurant/", include("restaurant.urls")),
    path("dashboard/", DashboardView.as_view(), name="root_dashboard"),
    path("menu/", MenuView.as_view(), name="customer_menu"),
    path("", RedirectView.as_view(pattern_name="root_dashboard", permanent=True)),
    path('', include('pwa.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
