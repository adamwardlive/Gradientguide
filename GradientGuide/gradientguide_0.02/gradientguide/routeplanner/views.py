from django.shortcuts import render, redirect, get_object_or_404
from .forms import TrainingSessionForm
from .utils import calculate_distance
from .models import TrainingSession
from django.urls import reverse
from django.http import JsonResponse
import requests
import json

def session_input(request):
    if request.method == 'POST':
        form = TrainingSessionForm(request.POST)
        if form.is_valid():
            session = form.save()
            distance = calculate_distance(session.power, session.duration)
            # Redirect to the session detail page with the session's ID
            return redirect('session_detail', session_id=session.id)
    else:
        form = TrainingSessionForm()
    return render(request, 'routeplanner/session_input.html', {'form': form})

def session_detail(request, session_id):
    session = get_object_or_404(TrainingSession, id=session_id)
    distance = calculate_distance(session.power, session.duration)

    start_lng = -74.50 + session.power * 0.01
    start_lat = 40 + session.duration * 0.01
    end_lng = start_lng + 0.5  # Adjust based on your requirements
    end_lat = start_lat + 0.5  # Adjust based on your requirements

    mapbox_url = f"https://api.mapbox.com/directions/v5/mapbox/cycling/{start_lng},{start_lat};{end_lng},{end_lat}"
    mapbox_params = {
        'access_token': 'pk.eyJ1IjoiYWRhbXdhcmRoYnUiLCJhIjoiY2x1MTZ3dmRxMGZ1aDJuczNjczVoOXMybSJ9.EN8pBBjC6P76HNPCSpnu_g',  # Make sure to use your actual token
        'geometries': 'geojson'
    }
    response = requests.get(mapbox_url, params=mapbox_params)
    route_data = {}

    if response.status_code == 200:
        # Extract the geometry of the first route from the response
        data = response.json()
        route_data = data['routes'][0]['geometry'] if data['routes'] else {}

    return render(request, 'routeplanner/session_detail.html', {
        'session': session,
        'distance': distance,
        'route_data': json.dumps(route_data)  # Pass the route geometry as a JSON string
    })

def show_map(request):
    # This view simply renders the map.html template
    return render(request, 'map.html')


def geocode_location(location_name):
    API_KEY = 'pk.eyJ1IjoiYWRhbXdhcmRoYnUiLCJhIjoiY2x1MTZ3dmRxMGZ1aDJuczNjczVoOXMybSJ9.EN8pBBjC6P76HNPCSpnu_g'
    base_url = "https://api.mapbox.com/geocoding/v5/mapbox.places"
    search_url = f"{base_url}/{location_name}.json?access_token={API_KEY}"
    response = requests.get(search_url)
    if response.status_code == 200:
        data = response.json()
        if data['features']:  # Check if the features list is not empty
            longitude, latitude = data['features'][0]['center']
            return latitude, longitude
        else:
            raise ValueError("No geocoding results found for the location provided.")
    else:
        raise Exception("Geocoding request failed with status code:", response.status_code)


def calculate_route(request):
    if request.method == 'POST':
        weight = request.POST.get('weight')
        speed = request.POST.get('speed')
        starting_location = request.POST.get('starting_location')  # Retrieve the starting location from the request

        # Geocode the starting location to get start_lat and start_lng
        start_lat, start_lng = geocode_location(starting_location)

        # Example logic to calculate ending coordinates based on some parameters (adjust as needed)
        end_lng = start_lng + 0.5
        end_lat = start_lat + 0.5

        # Construct the Mapbox Directions API URL
        mapbox_url = f"https://api.mapbox.com/directions/v5/mapbox/cycling/{start_lng},{start_lat};{end_lng},{end_lat}"
        mapbox_params = {
            'access_token': 'pk.eyJ1IjoiYWRhbXdhcmRoYnUiLCJhIjoiY2x1MTZ3dmRxMGZ1aDJuczNjczVoOXMybSJ9.EN8pBBjC6P76HNPCSpnu_g',  # Replace with your actual access token
            'geometries': 'geojson',
            'roundtrip': 'true',  # Ensure the route is a roundtrip
            'source': 'first',  # Start at the first location
            'destination': 'first' 
        }
        response = requests.get(mapbox_url, params=mapbox_params)

        if response.status_code == 200:
            # Extract the route data from the response
            route_data = response.json()
            return JsonResponse({'route': route_data}, safe=False)
        else:
            return JsonResponse({'error': 'Failed to fetch the route from Mapbox.'}, status=response.status_code)

    # Redirect to the map view if it's not a POST request
    return redirect('show_map')

# Home page view
def home(request):
    return render(request, 'routeplanner/home.html')

# Build a Route view
def new_session(request):
    # Your existing logic for new session will go here
    pass

def past_routes(request):
    sessions = TrainingSession.objects.all()
    session_data = []
    for session in sessions:
        try:
            start_lat, start_lng = geocode_location(session.starting_location)
            end_lng = start_lng + 0.5  # Adjust based on your requirements
            end_lat = start_lat + 0.5  # Adjust based on your requirements
            mapbox_url = f"https://api.mapbox.com/directions/v5/mapbox/cycling/{start_lng},{start_lat};{end_lng},{end_lat}"
            mapbox_params = {
                'access_token': 'pk.eyJ1IjoiYWRhbXdhcmRoYnUiLCJhIjoiY2x1MTZ3dmRxMGZ1aDJuczNjczVoOXMybSJ9.EN8pBBjC6P76HNPCSpnu_g',
                'geometries': 'geojson'
            }
            response = requests.get(mapbox_url, params=mapbox_params)
            if response.status_code == 200:
                data = response.json()
                route_data = data['routes'][0]['geometry'] if data['routes'] else {}
                session_data.append({
                    'session': session,
                    'route_data': json.dumps(route_data)
                })
            else:
                session_data.append({
                    'session': session,
                    'route_data': json.dumps({})
                })
        except ValueError as e:
            session_data.append({
                'session': session,
                'error_message': str(e),
                'route_data': json.dumps({})
            })
    return render(request, 'routeplanner/past_routes.html', {'session_data': session_data})


def delete_session(request, session_id):
    session = get_object_or_404(TrainingSession, id=session_id)
    session.delete()
    return redirect('past_routes')  # Redirect to the past routes view after deletion

def edit_session(request, session_id):
    if request.method == 'POST':
        session = get_object_or_404(TrainingSession, id=session_id)
        data = json.loads(request.body)
        session.name = data.get('name', session.name)  # Fallback to existing name if not provided
        session.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid method'}, status=405)

# User Profile view
def user_profile(request):
    # Logic for user profile update will go here
    pass