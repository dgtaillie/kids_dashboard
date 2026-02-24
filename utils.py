import os
import requests
from datetime import datetime
import pytz
import googlemaps


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



def get_forecast(city="Olney", units="imperial"):
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


def commute_times_multi_route(ORIGIN_ADDRESS, DESTINATION_ADDRESS):
    # Initialize client with API key
    gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

    # Define locations
    origin = ORIGIN_ADDRESS
    destination = DESTINATION_ADDRESS

    # Request directions with alternatives
    now = datetime.now()
    directions_result = gmaps.directions(
        origin,
        destination,
        mode="driving",
        departure_time=now,
        alternatives=True,
    )

    # Collect commute times for all routes
    views = []
    for i, route in enumerate(directions_result):
        views.append(f"Via {route['summary']}: {route['legs'][0]['duration']['text']}")

    return views
