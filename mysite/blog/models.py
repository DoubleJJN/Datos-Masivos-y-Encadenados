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
