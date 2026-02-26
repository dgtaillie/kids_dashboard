import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
from utils import get_current_time, get_weather, get_forecast, commute_times_multi_route, ORIGIN_ADDRESS, DESTINATION_ADDRESS

# Initialize Dash app with a Bootstrap theme
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.CYBORG],
    suppress_callback_exceptions=True,
)

# ----------------------------------------------------------------------
# Layout
# ----------------------------------------------------------------------
app.layout = dbc.Container(
    [
        # Header
        dbc.Row(
            dbc.Col(
                html.H1(
                    "🚀 Taillie's Dashboard",
                    className="text-center",
                    style={"marginTop": "20px", "marginBottom": "30px"},
                )
            )
        ),
        # Top Row
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H2("Current Weather", className="card-title"),
                                html.Img(
                                    id="weather-icon",
                                    src="",
                                    style={"height": "80px", "marginBottom": "10px"},
                                ),
                                html.H3(id="weather-temp", className="card-text"),
                                html.P(id="weather-desc", className="card-text"),
                                html.P(id="weather-wind", className="card-text"),
                                dcc.Interval(
                                    id="weather-interval",
                                    interval=5 * 60 * 1000,
                                    n_intervals=0,
                                ),
                            ]
                        ),
                        className="card",
                    ),
                    width=12,
                    md=4,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H2("Current Time", className="card-title"),
                                html.H3(id="time-display", className="card-text"),
                                dcc.Interval(id="time-interval", interval=1000, n_intervals=0),
                            ]
                        ),
                        className="card",
                    ),
                    width=12,
                    md=4,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H2("Sara Work Commute", className="card-title"),
                                html.Div(id="commute-table", className="card-text"),
                                dcc.Interval(
                                    id="commute-interval", interval=5 * 60 * 1000, n_intervals=0
                                ),
                            ]
                        ),
                        className="card",
                    ),
                    width=12,
                    md=4,
                ),
            ]
        ),
        # Bottom Row
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                        html.H2("Forecast", className="card-title"),
                                        html.Img(
                                            id="forecast-icon",
                                            src="",
                                            style={"height": "80px", "marginBottom": "10px"},
                                        ),
                                        html.H3(id="forecast-temp", className="card-text"),
                                        html.P(id="forecast-highlow", className="card-text"),
                                        html.P(id="forecast-desc", className="card-text"),
                                        html.P(id="forecast-wind", className="card-text"),
                                        dcc.Interval(
                                            id="forecast-interval",
                                            interval=5 * 60 * 1000,
                                            n_intervals=0,
                                        ),
                            ]
                        ),
                        className="card",
                    ),
                    width=12,
                    md=4,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H2("", className="card-title"),
                html.A(
                    html.Img(
                        src="https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg",
                        style={"height": "160px"},
                    ),
                    href="https://open.spotify.com",
                    target="_blank",
                )
                            ]
                        ),
                        className="card",
                    ),
                    width=12,
                    md=4,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H2("Placeholder 2", className="card-title"),
                                # Add content later
                            ]
                        ),
                        className="card",
                    ),
                    width=12,
                    md=4,
                ),
            ]
        ),
    ],
    fluid=True,
)


# ----------------------------------------------------------------------
# Callbacks
# ----------------------------------------------------------------------
@app.callback(Output("time-display", "children"), Input("time-interval", "n_intervals"))
def update_time(_):
    """Update the displayed time every second."""
    return get_current_time()


@app.callback(
    Output("weather-temp", "children"),
    Output("weather-desc", "children"),
    Output("weather-wind", "children"),
    Output("weather-icon", "src"),
    Input("weather-interval", "n_intervals"),
)
def update_weather(_):
    """Fetch weather data and update the card."""
    data = get_weather()
    icon_url = f"http://openweathermap.org/img/wn/{data['icon']}@2x.png"
    wind_info = f"Wind: {data['wind_speed']} kn, {data['wind_deg']}°"
    return f"{data['temp']}°F", data["description"], wind_info, icon_url


@app.callback(
    Output("forecast-temp", "children"),
    Output("forecast-highlow", "children"),
    Output("forecast-desc", "children"),
    Output("forecast-wind", "children"),
    Output("forecast-icon", "src"),
    Input("forecast-interval", "n_intervals"),
)
def update_forecast(_):
    """Fetch forecast data and update the card."""
    data = get_forecast()
    icon_url = f"http://openweathermap.org/img/wn/{data['icon']}@2x.png"
    wind_info = f"Wind: {data['wind_speed']} kn, {data['wind_deg']}°"
    high_low = f"{data['temp_max']}°F / {data['temp_min']}°F"
    return (
        f"{data['temp']}°F",
        high_low,
        data["description"],
        wind_info,
        icon_url,
    )
@app.callback(
    Output("commute-table", "children"),
    Input("commute-interval", "n_intervals"),
)
def update_commute(_):
    """Fetch multi‑route commute information and display as table."""
    routes = commute_times_multi_route(ORIGIN_ADDRESS, DESTINATION_ADDRESS)
    rows = []
    for route in routes:
        # Expected format "Via X: Y"
        parts = route.split(":")
        summary = parts[0].replace("Via", "").strip()
        duration = parts[1].strip() if len(parts) > 1 else ""
        rows.append(html.Tr([html.Td(summary), html.Td(duration)]))
    return html.Table([
        html.Thead(html.Tr([html.Th("Route"), html.Th("Duration")])),
        html.Tbody(rows)
    ])


# ----------------------------------------------------------------------
# Run server
# ----------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)