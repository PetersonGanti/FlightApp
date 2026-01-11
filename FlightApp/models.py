from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Flight(models.Model):
    flight_number = models.CharField(max_length=10)
    airline = models.CharField(max_length=50)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    price = models.FloatField()

    def _str_(self):
        return f"{self.flight_number} - {self.source} to {self.destination}"



class Booking(models.Model):
    SEAT_CLASS_CHOICES = [
        ('Economy', 'Economy'),
        ('Business', 'Business'),
        ('First Class', 'First Class'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey('Flight', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=15)
    seats = models.PositiveIntegerField(default=1)
    seat_class = models.CharField(max_length=20, choices=SEAT_CLASS_CHOICES, default='Economy')
    passenger_names = models.TextField(blank=True)  # or JSONField in future
    passenger_ages = models.TextField(blank=True)
    journey_date = models.DateField(null=True, blank=True)  # default=timezone.now if needed
    booked_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.full_name} - {self.flight.flight_number}"