# Django serializers.py
from rest_framework import serializers
from .models import Seat, Reservation


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['seat_number']


class ReservationSerializer(serializers.ModelSerializer):
    cabin_class = serializers.SerializerMethodField()
    seats = SeatSerializer(many=True)

    class Meta:
        model = Reservation
        fields = ['reservation_id', 'cabin_class', 'seats', 'total_fare']

    def get_cabin_class(self, obj):
        return obj.cabin.class_name