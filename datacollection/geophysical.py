import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

def getweatherdata(latitude, longitude, start_date="2023-01-01", end_date="2025-01-01"):
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    
    url = "https://historical-forecast-api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": ["temperature_2m", "relative_humidity_2m", "precipitation", "uv_index"]
    }

    # Fetch the weather data
    responses = openmeteo.weather_api(url, params=params)
    
    # Process the first location's response
    response = responses[0]

    # Process hourly data
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

    hourly_data = {
        "date": pd.date_range(
            start = pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end = pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq = pd.Timedelta(seconds=hourly.Interval()),
            inclusive = "left"
        ),
        "temperature_2m": hourly_temperature_2m
    }

    hourly_dataframe = pd.DataFrame(data=hourly_data)
    return hourly_dataframe