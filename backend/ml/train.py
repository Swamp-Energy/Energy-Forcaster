import os
from darts.models import NBEATSModel
from darts.utils.split import train_test_split
from model import load_data, create_model

# File paths
DATA_PATH = os.path.join('data', 'energy_data.csv')
MODEL_SAVE_PATH = os.path.join('models', 'nbeats_model.pth')

def train():
    # Load the data
    series = load_data(DATA_PATH)

    # Split the data into train and test sets
    train, val = train_test_split(series, test_size=0.2)

    # Create the model
    model = create_model(input_chunk_length=24, output_chunk_length=12)

    # Train the model
    print("Training the model...")
    model.fit(train)

    # Save the model
    print(f"Saving the model to {MODEL_SAVE_PATH}...")
    model.save(MODEL_SAVE_PATH)
    print("Training complete!")

if __name__ == "__main__":
    train()
