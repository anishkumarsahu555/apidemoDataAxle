# Django tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Seat, Cabin, Reservation
from .views import calculate_total_fare


class SeatReservationAPITest(APITestCase):
    def test_seat_reservation_success(self):
        # test data for available seats
        cabin = Cabin.objects.create(class_name='first_class')
        Seat.objects.create(cabin=cabin, seat_number=1, is_available=True)
        Seat.objects.create(cabin=cabin, seat_number=2, is_available=True)

        # Initiating seat reservation process and providing family members count.
        data = {'num_family_members': 2, 'preferred_cabin_class': 'first_class'}
        url = reverse('reserve_seat')
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Seat.objects.filter(is_available=False).count(), 2)

        # Validate reservation details, total fare, and reservation number
        reservation = Reservation.objects.get(reservation_id=response.data['reservation_id'])
        self.assertEqual(reservation.total_fare, calculate_total_fare(2, 'first_class'))
        self.assertIsNotNone(reservation.reservation_id)

    def test_seat_reservation_insufficient_seats(self):
        # Create test data for available seats
        cabin = Cabin.objects.create(class_name='second_class')
        Seat.objects.create(cabin=cabin, seat_number=1, is_available=True)

        # Initiating seat reservation process and providing family members count.
        data = {'num_family_members': 4, 'preferred_cabin_class': 'second_class'}
        url = reverse('reserve_seat')
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Seat.objects.filter(is_available=False).count(), 0)
