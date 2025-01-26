import os
from darts.models import NBEATSModel
from darts import TimeSeries
from darts.utils.timeseries_generation import datetime_attribute_timeseries
from model import load_data, create_model

# File paths
DATA_PATH = os.path.join('data', 'energy_data.csv')
MODEL_SAVE_PATH = os.path.join('models', 'nbeats_model.pth')

def train():
    # Load the data and covariates
    series, covariates = load_data(DATA_PATH)

    # Debugging: Check type and length
    print("Type of series:", type(series))
    print("Length of the TimeSeries:", len(series))

    # Split the data into train and validation sets
    if len(series) > 10:  # Ensure there's enough data to split
        train, val = series.split_after(0.8)
        train_cov, val_cov = covariates.split_after(0.8)
    else:
        raise ValueError("Not enough data to split into train and validation sets.")

    # Create the model
    model = create_model(input_chunk_length=24, output_chunk_length=12)

    # Train the model with covariates
    print("Training the model...")
    model.fit(series=train, past_covariates=train_cov)

    # Save the model
    print(f"Saving the model to {MODEL_SAVE_PATH}...")
    model.save(MODEL_SAVE_PATH)
    print("Training complete!")

if __name__ == "__main__":
    train()
