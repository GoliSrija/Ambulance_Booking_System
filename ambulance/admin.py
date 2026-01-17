from django.contrib import admin
from .models import Ambulance, Driver, AmbulanceBooking

admin.site.register(Ambulance)
admin.site.register(Driver)
admin.site.register(AmbulanceBooking)
