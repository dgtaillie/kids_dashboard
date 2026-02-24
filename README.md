# Kid‑Friendly Daily Dashboard

A simple, colorful dashboard built with **Dash** that shows:

- **Current time** (updates every second)  
- **Weather** for **Washington DC** (OpenWeatherMap)  
- **Commute time** (Google Maps Distance Matrix)

The UI uses a playful “kid‑friendly” style with large fonts, bright colors, and cartoon‑like icons.

## Features

- Real‑time clock
- Weather card with temperature, description, and icon
- Commute card with travel time and distance
- Automatic refresh (time every second, weather & commute every 5 minutes)
- Easy to customize API keys, locations, and styling

## Prerequisites

- **Python 3.9+** (tested on Windows 11)
- **OpenWeatherMap API key** (you already have one)
- **Google Maps Distance Matrix API key** (you already have one)

## Setup

```bash
# 1️⃣ Clone or copy the project folder
cd kid_dashboard

# 2️⃣ (Optional) Create a virtual environment
python -m venv venv
venv\Scripts\activate   # Windows

# 3️⃣ Install dependencies
pip install -r requirements.txt
```

## Configuration

Edit `kid_dashboard/utils.py` and replace the placeholder strings with your real values:

```python
# utils.py
OPENWEATHER_API_KEY = "YOUR_OPENWEATHER_API_KEY"
GOOGLE_MAPS_API_KEY = "YOUR_GOOGLE_MAPS_API_KEY"

ORIGIN_ADDRESS = "YOUR_ORIGIN_ADDRESS"
DESTINATION_ADDRESS = "YOUR_DESTINATION_ADDRESS"
```

- **Weather**: The city is hard‑coded to `Olney, MD`. Change the arguments in `get_weather()` if you need a different location.
- **Commute**: Set `ORIGIN_ADDRESS` and `DESTINATION_ADDRESS` to the addresses you want to measure.

## Run the Dashboard

```bash
python app.py
```

Open a browser and navigate to **http://127.0.0.1:8050**. You should see a bright, kid‑styled dashboard with the current time, weather, and commute information.

## Customising the Look

All styling lives in `kid_dashboard/assets/kid_style.css`. Feel free to edit colors, fonts, or layout. The file is automatically loaded by Dash because it resides in the `assets/` folder.

## Troubleshooting

- **Missing icons** – Ensure you have internet access; weather icons are fetched from OpenWeatherMap.
- **API errors** – Double‑check that your API keys are correct and that the services are enabled for your account.
- **Port already in use** – Change the port in `app.run_server(debug=True, port=8051)` if needed.

Enjoy your colorful, kid‑friendly dashboard! 🚀
