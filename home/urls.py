# Django urls.py
from django.urls import path
from .views import SeatReservationView

urlpatterns = [
    path('reserve_seat/', SeatReservationView.as_view(), name='reserve_seat'),
]
