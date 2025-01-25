from pymongo import MongoClient
from dotenv import load_dotenv
from pymongo.operations import UpdateOne
import pandas as pd
import os

load_dotenv()
uri = os.getenv("MONGODB_URI")
client = MongoClient(uri)

def getcitylocations():
    db = client["Cities"]
    collection = db["Positional-Data"]

    script_dir = os.path.dirname(__file__)
    csv_path = os.path.join(script_dir, 'uscities.csv')
    df = pd.read_csv(csv_path, skiprows=1, usecols=[1,2,6,7])
    df.columns = ['city', 'state', 'latitude', 'longitude']

    cities = df.to_dict('records')
    
    bulk_ops = [UpdateOne(
        {'city': city['city'], 'state': city['state']},
        {'$set': city},
        upsert=True
    ) for city in cities]
    
    result = collection.bulk_write(bulk_ops)


if __name__ == "__main__":
    getcitylocations()