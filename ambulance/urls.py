from django.urls import path
from . import views

app_name = 'ambulance'

urlpatterns = [
    path('book/', views.book_ambulance, name='book'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('driver-bookings/', views.driver_bookings, name='driver_bookings'),
    path('accept/<int:booking_id>/', views.accept_booking, name='accept_booking'),
    path(
        'update-status/<int:booking_id>/<str:status>/',
        views.update_status,
        name='update_status'
    ),
    path(
    'update-location/<int:booking_id>/',
    views.update_location,
    name='update_location'
),
path('track/<int:booking_id>/', views.track_booking, name='track_booking'),


]
