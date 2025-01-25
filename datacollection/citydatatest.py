from geophysical import getweatherdata
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
uri = os.getenv("MONGODB_URI")
client = MongoClient(uri)

def gethourlydata():
    db = client["Cities"]
    collection = db["Positional Data"]
    
    cities = collection.find({})
    
    for city in cities:
        print(f"{city['city']}, {city['state']}: ({city['latitude']}, {city['longitude']})")

if __name__ == "__main__":
    gethourlydata()