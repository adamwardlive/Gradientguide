# utils.py

def find_optimal_routes(user_preferences, available_routes):
    """
    Finds routes that best match the user's preferences.

    Parameters:
    - user_preferences: dict containing preferences such as 'desired_distance' and 'max_elevation_gain'.
    - available_routes: list of dicts, each representing a route with properties like 'distance', 'elevation_gain', and 'safety_rating'.

    Returns:
    - list of dicts: optimized routes that match the user preferences.
    """
    optimized_routes = []

    for route in available_routes:
        # Basic filtering based on distance and elevation gain
        if route['distance'] >= user_preferences['desired_distance'] and route['elevation_gain'] <= user_preferences['max_elevation_gain']:
            optimized_routes.append(route)

    # Further optimization logic can be added here, such as considering safety ratings, user reviews, or more complex algorithms

    return optimized_routes

