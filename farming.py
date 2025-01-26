import os
import json
import numpy as np
import pandas as pd
import random
from datetime import datetime, timedelta

script_dir = os.path.dirname(os.path.abspath(__file__))

json_path = os.path.join(script_dir, 'city_data.json')

with open(json_path, 'r') as f:
    city_data = json.load(f)

def get_seasonal_multiplier(month):
    if month in [12, 1, 2]:  
        return 1.3  
    elif month in [6, 7, 8]:  
        return 1.5  
    else:  
        return 1.1  

hourly_multipliers = {
    "residential": [
        0.6, 0.5, 0.4, 0.4, 0.5, 0.8, 1.2, 1.1, 1.0, 0.8, 0.7, 0.6,  
        0.7, 0.8, 0.9, 1.0, 1.1, 1.3, 1.5, 1.4, 1.2, 1.1, 0.9, 0.7   
    ],
    "commercial": [
        0.3, 0.2, 0.2, 0.2, 0.3, 0.5, 0.8, 1.0, 1.2, 1.3, 1.2, 1.1,  
        1.1, 1.2, 1.3, 1.5, 1.4, 1.3, 1.2, 1.0, 0.8, 0.6, 0.4, 0.3   
    ]
}

def is_holiday(date):
    holidays = [
        "01/01",  
        "07/04", 
        "12/25",  
        "11/25",  
    ]
    return date.strftime("%m/%d") in holidays or (date.month == 11 and date.weekday() == 3 and 22 <= date.day <= 28)

def generate_hourly_energy_usage(city_data, years=2):
    data = []

    start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=365 * years)
    end_date = start_date + timedelta(days=365 * years)

    current_time = start_date
    while current_time < end_date:
        for city in city_data:
            state = city["state"]
            city_name = city["city"]
            population = city["population"]
            avg_energy = city["avg_energy_per_person"]

            month = current_time.month
            hour = current_time.hour
            weekday = current_time.weekday()

            seasonal_multiplier = get_seasonal_multiplier(month)
            hour_multiplier = hourly_multipliers["residential" if hour < 6 or hour >= 18 else "commercial"][hour]

           
            if weekday >= 5:  
                weekend_multiplier = 1.1  
            else:
                weekend_multiplier = 1.0  

            if is_holiday(current_time):
                holiday_multiplier = 1.2  
            else:
                holiday_multiplier = 1.0

            base_usage = population * avg_energy * seasonal_multiplier * hour_multiplier * weekend_multiplier * holiday_multiplier

            noise = random.uniform(-0.05, 0.05) * base_usage
            hourly_usage = base_usage + noise

            data.append({
                "timestamp": current_time.strftime("%Y-%m-%d %H:%M"),
                "state": state,
                "city": city_name,
                "population": population,
                "hourly_energy_usage": round(hourly_usage, 2)
            })

        current_time += timedelta(hours=1)

    return data

energy_data = generate_hourly_energy_usage(city_data, years=2)

energy_df = pd.DataFrame(energy_data)

energy_df.sort_values(by=["city", "timestamp"], inplace=True)

csv_path = os.path.join(script_dir, 'hourly_energy_usage_2_years.csv')
energy_df.to_csv(csv_path, index=False)

print(f"Realistic energy usage data for 2 years generated, sorted, and saved to '{csv_path}'.")