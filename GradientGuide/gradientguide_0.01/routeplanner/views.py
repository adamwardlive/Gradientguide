# In your views.py file

from django.shortcuts import render
from .utils import find_optimal_routes
from .models import Route

def route_suggestions(request):
    if request.method == 'POST':
        # Extract user preferences from the POST request
        user_preferences = {
            'desired_distance': request.POST.get('desired_distance'),
            'max_elevation_gain': request.POST.get('max_elevation_gain')
        }

        # For demonstration, assume available_routes is fetched from the database
        # In a real application, you would fetch this data from your Route model
        available_routes = Route.objects.all()

        # Convert QuerySet to list of dicts for the optimization function
        available_routes_dicts = list(available_routes.values())

        optimized_routes = find_optimal_routes(user_preferences, available_routes_dicts)
        return render(request, 'route_suggestions.html', {'routes': optimized_routes})
    else:
        # Display the form for user input if the request is not POST
        return render(request, 'route_form.html')


