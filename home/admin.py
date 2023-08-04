from django.contrib import admin
from .models import Seat, Cabin, Reservation
# Register your models here.

admin.site.register(Seat)
admin.site.register(Cabin)
admin.site.register(Reservation)
