# populate_test_data.py
from datetime import timedelta
import os
import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from routeplanner.models import User, Route, TrainingSession, UserProfile

class Command(BaseCommand):
    help = "Populate the database with test data"

    def handle(self, *args, **options):
        # Create test users
        for i in range(10):  # Create 10 users
            username = f'user_{i}'
            user = User.objects.create_user(username=username, email=f'{username}@example.com', password='password')
            UserProfile.objects.create(user=user, bio=f'Bio of {username}', fitness_goals='Run a marathon')

        # Create test routes
        for i in range(5):  # Create 5 routes
            Route.objects.create(
                name=f'Route {i}',
                distance=random.uniform(5.0, 20.0),  # Random distance between 5km and 20km
                elevation_gain=random.uniform(100.0, 500.0),  # Random elevation gain between 100m and 500m
                safety_rating=random.randint(1, 5),  # Random safety rating between 1 and 5
                created_by=User.objects.order_by('?').first()  # Random user
            )

        # Create test training sessions
        for i in range(20):  # Create 20 training sessions
            user = User.objects.order_by('?').first()
            route = Route.objects.order_by('?').first()
            TrainingSession.objects.create(
                user=user,
                route=route,
                date=timezone.now().date(),
                duration=timedelta(minutes=random.randint(30, 180)),  # Random duration between 30 and 180 minutes
                average_speed=random.uniform(10.0, 40.0),  # Random average speed between 10km/h and 40km/h
                power_output=random.uniform(200.0, 400.0)  # Random power output between 200W and 400W
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))
