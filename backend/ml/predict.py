import os
from darts import TimeSeries
from model import load_data
from darts.models import NBEATSModel
import matplotlib.pyplot as plt

# File paths
DATA_PATH = os.path.join('data', 'energy_data.csv')
MODEL_SAVE_PATH = os.path.join('models', 'nbeats_model.pth')

def predict():
    # Load the data
    series = load_data(DATA_PATH)

    # Load the trained model
    model = NBEATSModel.load(MODEL_SAVE_PATH)

    # Make predictions
    print("Making predictions...")
    forecast = model.predict(n=12, series=series)

    # Plot the results
    series.plot(label='Actual')
    forecast.plot(label='Forecast')
    plt.legend()
    plt.title("Energy Consumption Forecast")
    plt.show()

if __name__ == "__main__":
    predict()
