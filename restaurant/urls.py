from django.urls import path
from .views import MenuView

app_name = 'restaurant'

urlpatterns = [
    path('menu/', MenuView.as_view(), name='menu'),
]
