from django.db import models
from django.conf import settings
from django.utils import timezone


class Ambulance(models.Model):
    vehicle_number = models.CharField(max_length=50, unique=True)
    driver_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    location = models.CharField(max_length=255)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.vehicle_number


class Driver(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    license_number = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


class AmbulanceBooking(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('On the way', 'On the way'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    # ------------------
    # RELATIONS
    # ------------------
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    ambulance = models.ForeignKey(
        Ambulance,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    driver = models.ForeignKey(
        Driver,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # ------------------
    # BOOKING DETAILS
    # ------------------
    pickup_location = models.CharField(max_length=200)
    drop_location = models.CharField(max_length=200)

    emergency_level = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
        ]
    )

    booking_time = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    # ------------------
    # REAL-TIME TRACKING (GPS DEMO + ADVANCED)
    # ------------------

    # Simple readable location (for demo & interview explanation)
    current_location = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    # GPS coordinates (advanced / future use)
    current_latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    current_longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    # Estimated Time of Arrival (minutes)
    eta_minutes = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    # Last time driver updated location
    last_location_update = models.DateTimeField(
        auto_now=True
    )

    # Notification message shown to patient
    notification_message = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['-booking_time']

    def __str__(self):
        return f"Booking #{self.id} - {self.user.username}"
