from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from ambulance.models import AmbulanceBooking, Driver
def home(request):
    return render(request, 'main/home.html')

@staff_member_required
def admin_dashboard(request):
    context = {
        'total_bookings': AmbulanceBooking.objects.count(),
        'pending_bookings': AmbulanceBooking.objects.filter(status='Pending').count(),
        'ongoing_bookings': AmbulanceBooking.objects.filter(status='On the way').count(),
        'completed_bookings': AmbulanceBooking.objects.filter(status='Completed').count(),
        'cancelled_bookings': AmbulanceBooking.objects.filter(status='Cancelled').count(),
        'drivers_count': Driver.objects.count(),
    }
    return render(request, 'main/admin_dashboard.html', context)




