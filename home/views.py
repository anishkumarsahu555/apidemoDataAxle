# Django views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Cabin, Seat, Reservation
from .serializers import  ReservationSerializer
import random
import string



def generate_reservation_number():
    # Generate a random alphanumeric reservation number of length 10
    length = 10
    characters = string.ascii_letters + string.digits
    reservation_number = ''.join(random.choice(characters) for i in range(length))
    return reservation_number

def calculate_total_fare(num_family_members, preferred_cabin_class):
    # Implementing calculation logic here based on the number of family members and cabin class with base fare of 50
    fare_per_member = 50
    total_fare = fare_per_member * num_family_members
    return total_fare

class SeatReservationView(APIView):
    def post(self, request):
        num_family_members = request.data.get('num_family_members')
        preferred_cabin_class = request.data.get('preferred_cabin_class')

        try:
            cabin = Cabin.objects.get(class_name=preferred_cabin_class)
        except Cabin.DoesNotExist:
            return Response("Invalid cabin class selected.", status=status.HTTP_400_BAD_REQUEST)

        #  Checking the availability of seats on the train.
        available_seats = Seat.objects.filter(cabin=cabin, is_available=True)

        if len(available_seats) < num_family_members:
            # Not enough seats available in the same cabin.
            return Response("Not enough seats available in the same cabin.", status=status.HTTP_400_BAD_REQUEST)

        #  Find a suitable arrangement to accommodate the entire family in the same cabin.
        reserved_seats = available_seats[:num_family_members]
        total_fare = calculate_total_fare(num_family_members, preferred_cabin_class)

        # Reserve the seats for the family members.
        for seat in reserved_seats:
            seat.is_available = False
            seat.save()

        # Generating a unique reservation ID and provide it to the user.
        reservation_number = generate_reservation_number()
        reservation = Reservation.objects.create(cabin=cabin, total_fare=total_fare, reservation_id=reservation_number)
        reservation.seats.set(reserved_seats)
        reservation.save()

        # Displaying the reservation details.
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
