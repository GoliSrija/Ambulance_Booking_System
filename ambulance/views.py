from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.utils import timezone
import random

from .models import AmbulanceBooking, Driver


# -----------------------
# ROLE HELPERS
# -----------------------
def is_patient(user):
    return hasattr(user, 'profile') and user.profile.role == 'patient'


def is_driver(user):
    return hasattr(user, 'profile') and user.profile.role == 'driver'


# -----------------------
# PATIENT: BOOK AMBULANCE
# -----------------------
@login_required(login_url='users:login')
def book_ambulance(request):

    if not is_patient(request.user):
        return HttpResponseForbidden("Only patients can book an ambulance.")

    if request.method == 'POST':
        pickup = request.POST.get('pickup_location')
        drop = request.POST.get('drop_location')
        emergency = request.POST.get('emergency_level')

        if not pickup or not drop:
            messages.error(request, "Pickup and Drop locations are required.")
            return redirect('ambulance:book')

        AmbulanceBooking.objects.create(
            user=request.user,
            pickup_location=pickup,
            drop_location=drop,
            emergency_level=emergency,
            status="Pending",
            notification_message="Booking created. Waiting for driver approval."
        )

        messages.success(request, "Ambulance booked successfully.")
        return redirect('ambulance:my_bookings')

    return render(request, 'ambulance/book.html')


# -----------------------
# PATIENT: VIEW BOOKINGS
# -----------------------
@login_required(login_url='users:login')
def my_bookings(request):

    if not is_patient(request.user):
        return redirect('users:dashboard')

    bookings = AmbulanceBooking.objects.filter(
        user=request.user
    ).order_by('-booking_time')

    return render(request, 'ambulance/my_bookings.html', {'bookings': bookings})


# -----------------------
# PATIENT: CANCEL BOOKING
# -----------------------
@login_required(login_url='users:login')
def cancel_booking(request, booking_id):

    booking = get_object_or_404(AmbulanceBooking, id=booking_id)

    if not is_patient(request.user):
        return HttpResponseForbidden("Only patients can cancel bookings.")

    if booking.user != request.user:
        messages.error(request, "You cannot cancel this booking.")
        return redirect('ambulance:my_bookings')

    if booking.status != "Pending":
        messages.error(request, "Only pending bookings can be cancelled.")
        return redirect('ambulance:my_bookings')

    booking.status = "Cancelled"
    booking.notification_message = "Booking cancelled by patient."
    booking.save()

    messages.success(request, "Booking cancelled successfully.")
    return redirect('ambulance:my_bookings')


# -----------------------
# DRIVER: VIEW BOOKINGS
# -----------------------
@login_required(login_url='users:login')
def driver_bookings(request):

    if not is_driver(request.user):
        messages.error(request, "Access denied.")
        return redirect('users:dashboard')

    bookings = AmbulanceBooking.objects.filter(
        driver__user=request.user
    ).exclude(status="Cancelled").order_by('-booking_time')

    return render(
        request,
        'ambulance/driver_bookings.html',
        {'bookings': bookings}
    )


# -----------------------
# DRIVER: ACCEPT BOOKING
# -----------------------
@login_required(login_url='users:login')
def accept_booking(request, booking_id):

    if not is_driver(request.user):
        return HttpResponseForbidden("Only drivers can accept bookings.")

    booking = get_object_or_404(
        AmbulanceBooking,
        id=booking_id,
        status="Pending",
        driver__isnull=True
    )

    driver = get_object_or_404(Driver, user=request.user)

    booking.driver = driver
    booking.status = "On the way"

    # Set ETA only once
    if booking.eta_minutes is None:
        booking.eta_minutes = 10

    booking.last_location_update = timezone.now()
    booking.notification_message = "Driver assigned. Ambulance is on the way."
    booking.save()

    messages.success(request, "Booking accepted successfully.")
    return redirect('ambulance:driver_bookings')


# -----------------------
# DRIVER: UPDATE STATUS
# -----------------------
@login_required(login_url='users:login')
def update_status(request, booking_id, status):

    if not is_driver(request.user):
        return HttpResponseForbidden("Access denied.")

    allowed_statuses = ['On the way', 'Completed']
    if status not in allowed_statuses:
        messages.error(request, "Invalid status.")
        return redirect('ambulance:driver_bookings')

    booking = get_object_or_404(
        AmbulanceBooking,
        id=booking_id,
        driver__user=request.user
    )

    if booking.status in ['Cancelled', 'Completed']:
        messages.error(request, "This booking cannot be updated.")
        return redirect('ambulance:driver_bookings')

    booking.status = status
    booking.last_location_update = timezone.now()

    if status == "Completed":
        booking.notification_message = "Trip completed. Patient reached destination."
    else:
        booking.notification_message = f"Status updated to {status}."

    booking.save()

    messages.success(request, f"Booking marked as {status}.")
    return redirect('ambulance:driver_bookings')


# -----------------------
# DRIVER: UPDATE LOCATION (GPS SIMULATION)
# -----------------------
@login_required(login_url='users:login')
def update_location(request, booking_id):

    if not is_driver(request.user):
        return HttpResponseForbidden("Only drivers can update location.")

    booking = get_object_or_404(
        AmbulanceBooking,
        id=booking_id,
        driver__user=request.user,
        status="On the way"
    )

    booking.current_latitude = round(random.uniform(17.35, 17.45), 6)
    booking.current_longitude = round(random.uniform(78.45, 78.55), 6)

    booking.last_location_update = timezone.now()
    booking.notification_message = "Ambulance is moving towards pickup location."
    booking.save()

    messages.success(request, "Location updated successfully.")
    return redirect('ambulance:driver_bookings')


# -----------------------
# PATIENT: TRACK BOOKING (MAP VIEW)
# -----------------------
@login_required(login_url='users:login')
def track_booking(request, booking_id):

    booking = get_object_or_404(
        AmbulanceBooking,
        id=booking_id,
        user=request.user
    )

    return render(
        request,
        'ambulance/track_booking.html',
        {'booking': booking}
    )
