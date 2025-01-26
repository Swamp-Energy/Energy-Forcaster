import pandas as pd
from pymongo import MongoClient, UpdateOne
import os
from datetime import datetime, timedelta
from geophysical import getweatherdata
from citylocations import getcitylocations

def merge_data(energy_csv_path, mongo_client):
   print("Starting data merge process...")
   
   energy_df = pd.read_csv(energy_csv_path, parse_dates=['timestamp'])
   print(f"Energy data loaded: {len(energy_df)} rows")
   
   cities_df = getcitylocations(mongo_client)
   print(f"City locations loaded: {len(cities_df)} rows")
   
   merged_df = pd.merge(
       energy_df,
       cities_df,
       on=['city'],
       how='inner'
   )
   print(f"Initial merge complete: {len(merged_df)} rows")
   
   weather_dfs = []
   i = 0
   for _, row in merged_df.iterrows():
       i += 1
       if i % 1000 == 0:
           print(i)
       try:
           weather_df = getweatherdata(
               row['latitude'],
               row['longitude'],
               start_date=row['timestamp'].strftime('%Y-%m-%d'),
               end_date=(row['timestamp'] + timedelta(days=1)).strftime('%Y-%m-%d')
           )
           # print(f"Weather data for {row['city']}: {weather_df.shape if weather_df is not None else None}")
           
           if weather_df is not None and not weather_df.empty:
               weather_df['city'] = row['city']
               weather_dfs.append(weather_df)
       except Exception as e:
           print(f"Error getting weather data for {row['city']}: {str(e)}")
   
   if not weather_dfs:
       raise ValueError("No weather data was retrieved for any city")
       
   weather_combined = pd.concat(weather_dfs, ignore_index=True)
   print(f"Combined weather data: {len(weather_combined)} rows")
   
   final_df = pd.merge(
       merged_df,
       weather_combined,
       on=['city'],
       how='inner'
   )
   print(f"Final merge complete: {len(final_df)} rows")
   
   return final_df

if __name__ == "__main__":
   uri = os.getenv("MONGODB_URI")
   client = MongoClient(uri)
   result_df = merge_data('hourly_energy_usage_2_years.csv', client)
   
   print("\nFirst 5 rows of final dataset:")
   print(result_df.head())
   result_df.to_csv('merged_2_data.csv', index=False)