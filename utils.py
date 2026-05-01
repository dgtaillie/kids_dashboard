import os
import requests
from datetime import datetime
import pytz



# Placeholder API keys – replace with your actual keys


# Locations – replace with your actual addresses
ORIGIN_ADDRESS = "ORIGIN ADDRESS"
DESTINATION_ADDRESS = "DESTINATION ADDRESS"

def get_current_time(timezone_str="America/New_York"):
    """
    Returns the current time as a formatted string in the given timezone.
    """
    tz = pytz.timezone(timezone_str)
    now = datetime.now(tz)
    return now.strftime("%I:%M %p")

def get_weather(city="Olney", units="imperial"):
    """
    Calls OpenWeatherMap API and returns a dict with temperature, description,
    wind speed (in knots) and wind direction (degrees).
    """
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&units={units}&appid={OPENWEATHER_API_KEY}"
    )
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        # Wind speed from API is in meters per second; convert to knots (1 m/s = 1.94384 knots)
        wind_speed_mps = data.get("wind", {}).get("speed", None)
        wind_speed_knots = (
            round(wind_speed_mps * 1.94384, 1) if isinstance(wind_speed_mps, (int, float)) else "N/A"
        )
        wind_deg = data.get("wind", {}).get("deg", "N/A")
        weather = {
            "temp": round(data["main"]["temp"]),
            "description": data["weather"][0]["description"].title(),
            "icon": data["weather"][0]["icon"],
            "wind_speed": wind_speed_knots,
            "wind_deg": wind_deg,
        }
        return weather
    except Exception as e:
        return {
            "temp": "N/A",
            "description": "Error",
            "icon": "01d",
            "wind_speed": "N/A",
            "wind_deg": "N/A",
        }



def get_forecast(city="Washington", units="imperial"):
    """
    Calls OpenWeatherMap 5 day / 3 hour forecast API and returns the first forecast entry.
    """
    url = (
        f"https://api.openweathermap.org/data/2.5/forecast"
        f"?q={city}&units={units}&appid={OPENWEATHER_API_KEY}"
    )
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        # Take the first forecast entry
        forecast = data["list"][0]
        wind_speed_mps = forecast.get("wind", {}).get("speed", None)
        wind_speed_knots = (
            round(wind_speed_mps * 1.94384, 1)
            if isinstance(wind_speed_mps, (int, float))
            else "N/A"
        )
        wind_deg = forecast.get("wind", {}).get("deg", "N/A")
        weather = {
            "temp": round(forecast["main"]["temp"]),
            "temp_min": round(forecast["main"]["temp_min"]),
            "temp_max": round(forecast["main"]["temp_max"]),
            "description": forecast["weather"][0]["description"].title(),
            "icon": forecast["weather"][0]["icon"],
            "wind_speed": wind_speed_knots,
            "wind_deg": wind_deg,
        }
        return weather
    except Exception as e:
        return {
            "temp": "N/A",
            "temp_min": "N/A",
            "temp_max": "N/A",
            "description": "Error",
            "icon": "01d",
            "wind_speed": "N/A",
            "wind_deg": "N/A",
        }




TOMTOM_API_KEY = "YOUR_TOMTOM_API_KEY"

def _geocode(address):
    """Convert an address string to 'lat,lon' using TomTom's geocoding API."""
    url = f"https://api.tomtom.com/search/2/geocode/{requests.utils.quote(address)}.json"
    resp = requests.get(url, params={"key": TOMTOM_API_KEY, "limit": 1})
    resp.raise_for_status()
    results = resp.json().get("results", [])
    if not results:
        raise ValueError(f"Could not geocode address: {address}")
    pos = results[0]["position"]
    return f"{pos['lat']},{pos['lon']}"


def _route_summary(route):
    """Extract a 'via X, Y' summary from a route's instructions."""
    roads = []
    seen = set()
    for leg in route.get("legs", []):
        for instr in leg.get("guidance", {}).get("instructions", []):
            road = instr.get("roadNumbers") or [instr.get("street")]
            for r in road:
                if r and r not in seen:
                    seen.add(r)
                    roads.append(r)
    # Keep the top 1-2 most prominent roads
    return ", ".join(roads[:2]) if roads else "unknown route"


def commute_times_multi_route(ORIGIN_ADDRESS, DESTINATION_ADDRESS):
    # Only run between 5am and 9am
    now = datetime.now()
    if not (5 <= now.hour < 9):
        return ["XX"]

    # Geocode origin and destination to coordinates
    origin = _geocode(ORIGIN_ADDRESS)
    destination = _geocode(DESTINATION_ADDRESS)

    # Request routes with alternatives, using live traffic
    url = f"https://api.tomtom.com/routing/1/calculateRoute/{origin}:{destination}/json"
    params = {
        "key": TOMTOM_API_KEY,
        "maxAlternatives": 2,
        "traffic": "true",
        "travelMode": "car",
        "routeType": "fastest",
        "departAt": "now",
        "instructionsType": "text",
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    routes = resp.json().get("routes", [])

    # Collect commute times for all routes
    views = []
    for route in routes:
        seconds = route["summary"]["travelTimeInSeconds"]
        minutes = round(seconds / 60)
        summary = _route_summary(route)
        views.append(f"Via {summary}: {minutes} min")

    return views
