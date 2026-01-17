from django.urls import path
from . import views

app_name = 'booking'   # ✅ REQUIRED for namespacing

urlpatterns = [
    path('create/', views.create_booking, name='create_booking'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    
]
