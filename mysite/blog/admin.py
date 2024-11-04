from django.contrib import admin
from .models import Destination, Accommodation, Activity, Itinerary, ItineraryActivity, Comment

admin.site.register(Destination)
admin.site.register(Accommodation)
admin.site.register(Activity)
admin.site.register(Itinerary)
admin.site.register(ItineraryActivity)
admin.site.register(Comment)