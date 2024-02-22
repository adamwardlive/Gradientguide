from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    # If you want to add additional fields to the user model, you can define them here
    # For example:
    # profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    # Overriding the groups and user_permissions fields to set a related_name
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="routeplanner_user_set",
        related_query_name="routeplanner_user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="routeplanner_user_set",
        related_query_name="routeplanner_user",
    )

class Route(models.Model):
    name = models.CharField(max_length=255)
    distance = models.FloatField(help_text="Distance in kilometers")
    elevation_gain = models.FloatField(help_text="Elevation gain in meters")
    safety_rating = models.IntegerField(help_text="Safety rating from 1 (low) to 5 (high)", null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_routes')

class TrainingSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='training_sessions')
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='training_sessions')
    date = models.DateField()
    duration = models.DurationField(help_text="Total duration of the training session")
    average_speed = models.FloatField(help_text="Average speed in km/h")
    power_output = models.FloatField(help_text="Average power output in watts", null=True, blank=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(null=True, blank=True)
    fitness_goals = models.TextField(null=True, blank=True)
    # Additional fields for user preferences, goals, etc.
