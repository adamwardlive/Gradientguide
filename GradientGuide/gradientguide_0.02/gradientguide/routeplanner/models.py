from django.db import models


class TrainingSession(models.Model):
    duration = models.IntegerField(help_text="Duration in minutes")
    power = models.IntegerField(help_text="Power in watts")
    weight = models.IntegerField(help_text="weight in kg")
    starting_location = models.CharField(max_length=255)
    # You can add more fields as needed, such as user references, timestamps, etc.

    def __str__(self):
        return f"{self.duration} mins at {self.power}W"
