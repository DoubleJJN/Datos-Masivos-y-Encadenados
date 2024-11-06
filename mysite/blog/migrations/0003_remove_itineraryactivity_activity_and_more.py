# Generated by Django 5.1.2 on 2024-11-05 22:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_accommodation_activity_comment_destination_itinerary_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itineraryactivity',
            name='activity',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='activity',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='accommodation',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='destination',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='user',
        ),
        migrations.RemoveField(
            model_name='itinerary',
            name='destination',
        ),
        migrations.RemoveField(
            model_name='itinerary',
            name='user',
        ),
        migrations.RemoveField(
            model_name='itineraryactivity',
            name='itinerary',
        ),
        migrations.DeleteModel(
            name='Activity',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Itinerary',
        ),
        migrations.DeleteModel(
            name='ItineraryActivity',
        ),
    ]
