from django.urls import path
from . import views

urlpatterns = [
    path('route-suggestions/', views.route_suggestions, name='route_suggestions'),
    # Add any other URLs for your app
]