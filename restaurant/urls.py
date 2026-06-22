from django.urls import path
from .views import MenuView, MorningResetView, EODReportView, DashboardView

app_name = 'restaurant'

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('menu/', MenuView.as_view(), name='menu'),
    path('morning-reset/', MorningResetView.as_view(), name='morning_reset'),
    path('eod-report/', EODReportView.as_view(), name='eod_report'),
]
