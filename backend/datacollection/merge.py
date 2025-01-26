import pandas as pd
from pymongo import MongoClient, UpdateOne
import os
from datetime import datetime, timedelta
from geophysical import getweatherdata
from citylocations import getcitylocations

from datetime import timedelta
import pandas as pd

pd.set_option('display.max_columns', None)

def merge_data(energy_csv_path, mongo_client):
    print("Starting data merge process...")
    
    energy_df = pd.read_csv(energy_csv_path, parse_dates=['timestamp'])
    cities_df = getcitylocations(mongo_client)
    
    merged_df = pd.merge(
        energy_df,
        cities_df,
        on=['city'],
        how='inner'
    )
    
    unique_cities = merged_df[['city', 'latitude', 'longitude']].drop_duplicates()
    print(f"Fetching weather data for {len(unique_cities)} unique cities...")
    
    weather_dfs = []
    for i, row in enumerate(unique_cities.itertuples(), start=1):
        try:
            weather_df = getweatherdata(
                row.latitude,
                row.longitude,
                start_date=merged_df['timestamp'].min().strftime('%Y-%m-%d'),
                end_date=merged_df['timestamp'].max().strftime('%Y-%m-%d')
            )
            
            if weather_df is not None and not weather_df.empty:
                weather_df['city'] = row.city
                weather_dfs.append(weather_df)
                
            print(f"Processed {i}/{len(unique_cities)} cities")
        except Exception as e:
            print(f"Error fetching weather data for {row.city}: {e}")
    
    if not weather_dfs:
        raise ValueError("No weather data was retrieved for any city")
    
    weather_combined = pd.concat(weather_dfs, ignore_index=True)
    weather_combined = weather_combined.rename(columns={'date': 'timestamp'})
    
    # Convert timestamps to UTC and remove timezone info
    weather_combined['timestamp'] = pd.to_datetime(weather_combined['timestamp']).dt.tz_convert('UTC').dt.tz_localize(None)
    merged_df['timestamp'] = pd.to_datetime(merged_df['timestamp']).dt.tz_localize('UTC').dt.tz_localize(None)
    
    final_df = pd.merge(
        merged_df,
        weather_combined,
        on=['city', 'timestamp'],
        how='inner'
    )
    
    print(f"\nFinal merge complete: {len(final_df)} rows")
    return final_df



if __name__ == "__main__":
   uri = os.getenv("MONGODB_URI")
   client = MongoClient(uri)
   result_df = merge_data('hourly_energy_usage_2_years.csv', client)
   
   print("\nFirst 5 rows of final dataset:")
   print(result_df.head())
   result_df.to_csv('merged_2_data.csv', index=False)
   print(getweatherdata(33.749, -84.388))