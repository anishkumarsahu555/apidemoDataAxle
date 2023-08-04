# models.py
from django.db import models

class Cabin(models.Model):
    class_name = models.CharField(max_length=50)

    def __str__(self):
        return self.class_name

class Seat(models.Model):
    cabin = models.ForeignKey(Cabin, on_delete=models.CASCADE)
    seat_number = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Cabin: {self.cabin}, Seat Number: {self.seat_number}, Available: {self.is_available}"

class Reservation(models.Model):
    reservation_id = models.CharField(max_length=10, unique=True)
    cabin = models.ForeignKey(Cabin, on_delete=models.CASCADE)
    seats = models.ManyToManyField(Seat)
    total_fare = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"Reservation ID: {self.reservation_id}, Cabin: {self.cabin}, Total Fare: {self.total_fare}"
