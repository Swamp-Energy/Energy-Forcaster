import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

def getweatherdata(latitude, longitude, start_date="2023-01-26", end_date="2025-01-24"):
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)
    
    url = "https://historical-forecast-api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": ["temperature_2m", "relative_humidity_2m", "precipitation", 
                   "visibility", "wind_speed_10m", "soil_temperature_0cm",
                   "soil_moisture_0_to_1cm", "uv_index", "is_day"]
    }

    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    hourly = response.Hourly()

    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        )
    }

    for idx, var in enumerate(params["hourly"]):
        hourly_data[var] = hourly.Variables(idx).ValuesAsNumpy()

    return pd.DataFrame(data=hourly_data)