from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import AmbulanceBooking
from ambulance.models import Ambulance

@login_required(login_url='users:login')
def create_booking(request):
    if request.method == "POST":
        pickup = request.POST['pickup']
        drop = request.POST['drop']
        emergency = request.POST['emergency']

        ambulance = Ambulance.objects.filter(is_available=True).first()

        if not ambulance:
            return render(request, 'booking/create_booking.html', {
                'error': 'No ambulances available right now'
            })

        AmbulanceBooking.objects.create(
            user=request.user,
            ambulance=ambulance,   # ✅ REQUIRED
            pickup_location=pickup,
            drop_location=drop,
            emergency_level=emergency
        )

        ambulance.is_available = False
        ambulance.save()

        return redirect('booking:my_bookings')

    return render(request, 'booking/create_booking.html')
@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'booking/my_bookings.html', {'bookings': bookings})
