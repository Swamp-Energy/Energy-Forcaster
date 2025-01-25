import pandas as pd
from model import create_forecast_model, make_predictions
import joblib
import os

# Define constants
DATA_PATH = 'data/energy_data.csv'  # Path to your dataset
MODEL_PATH = 'ml/saved_model.pkl'  # Path to save the trained model

def load_data(file_path):
    """
    Load dataset from a CSV file.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        DataFrame: Loaded data.
    """
    data = pd.read_csv(file_path)
    data['ds'] = pd.to_datetime(data['datetime'])  # Ensure datetime column is correct
    data['y'] = data['energy_consumption']  # Rename target column to 'y'
    return data[['ds', 'y']]

def train_and_save_model():
    """
    Train the model using historical data and save it to a file.
    """
    if not os.path.exists(DATA_PATH):
        print(f"Dataset not found at {DATA_PATH}")
        return

    # Load the dataset
    data = load_data(DATA_PATH)
    
    # Train the model
    print("Training the model...")
    model = create_forecast_model(data)
    
    # Save the model
    print(f"Saving the model to {MODEL_PATH}...")
    joblib.dump(model, MODEL_PATH)
    print("Model training complete and saved successfully!")

if __name__ == "__main__":
    train_and_save_model()
