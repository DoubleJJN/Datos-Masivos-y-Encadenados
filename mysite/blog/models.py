from django.db import models
from django.contrib.auth.models import User


# Country, city or main destination
class Destination(models.Model):
    name = models.CharField(max_length=100)
    english_name = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100)
    description = models.TextField()
    currency = models.CharField(max_length=10)
    language = models.CharField(max_length=50)
    timezone = models.CharField(max_length=10)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}, {self.city}, {self.country}"


# Hotels, hostels, airbnb, etc.
class Accommodation(models.Model):
    name = models.CharField(max_length=100)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} in {self.destination}"


# Theorical model in case we want to save the flights in the database
# Flights
# class Flight(models.Model):
#    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
#    airline = models.CharField(max_length=100)
#    departure_airport = models.CharField(max_length=100)
#    arrival_airport = models.CharField(max_length=100)
#    departure_date = models.DateField()
#    arrival_date = models.DateField()
#    number_of_people = models.IntegerField()
#    total_price = models.DecimalField(max_digits=10, decimal_places=2)
#
#    def __str__(self):
#        return f"Flight from {self.departure_airport} to {self.arrival_airport}"


# class Activity(models.Model):
#     destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     schedule = models.CharField(max_length=100)
#     rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
#     image_url = models.URLField(blank=True, null=True)

#     def __str__(self):
#         return f"{self.name} in {self.destination}"

# class Itinerary(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     destination = models.ForeignKey(Destination, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"Itinerary {self.name} by {self.user}"

# class ItineraryActivity(models.Model):
#     itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE)
#     activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
#     date = models.DateField()
#     time = models.TimeField()

#     def __str__(self):
#         return f"Activity {self.activity} in itinerary {self.itinerary}"


# class Comment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     destination = models.ForeignKey(Destination, on_delete=models.SET_NULL, null=True, blank=True)
#     accommodation = models.ForeignKey(Accommodation, on_delete=models.SET_NULL, null=True, blank=True)
#     activity = models.ForeignKey(Activity, on_delete=models.SET_NULL, null=True, blank=True)
#     comment = models.TextField()
#     rating = models.DecimalField(max_digits=3, decimal_places=2)
#     date = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return f"Comment by {self.user} - Rating: {self.rating}"

# class Booking(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE)
#     accommodation = models.ForeignKey(Accommodation, on_delete=models.SET_NULL, null=True, blank=True)
#     activity = models.ForeignKey(Activity, on_delete=models.SET_NULL, null=True, blank=True)
#     booking_date = models.DateField()
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.CharField(max_length=50, choices=[('confirmed', 'Confirmed'), ('pending', 'Pending'), ('cancelled', 'Cancelled')])

#     def __str__(self):
#         return f"Booking by {self.user} - Status: {self.status}"
