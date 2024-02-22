from django.contrib import admin
from .models import User, Route, TrainingSession, UserProfile

admin.site.register(User)
admin.site.register(Route)
admin.site.register(TrainingSession)
admin.site.register(UserProfile)