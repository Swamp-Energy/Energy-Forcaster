from darts.models import NBEATSModel
from darts import TimeSeries
import pandas as pd


def load_data(file_path: str) -> tuple:
    """
    Load and prepare the dataset with additional covariates.
    Returns the main series and covariates.
    """
    df = pd.read_csv(file_path, parse_dates=['datetime'])
    # df.set_index('datetime', inplace=True)
    print("Columns in the DataFrame:", df.columns)

    # Create TimeSeries object for the main energy consumption series
    series = TimeSeries.from_dataframe(df, 'datetime', 'energy_consumption')

    # Create TimeSeries for covariates (e.g., temperature, humidity, population)
    covariates = TimeSeries.from_dataframe(
        df, 'datetime', ['temperature', 'humidity', 'population']
            )

    return series, covariates


def create_model(input_chunk_length: int, output_chunk_length: int) -> NBEATSModel:
    """
    Define and return a Darts N-BEATS model.
    """
    model = NBEATSModel(
        input_chunk_length=input_chunk_length,
        output_chunk_length=output_chunk_length,
        n_epochs=10,  # Number of epochs to train
        random_state=42
    )
    return model


# def train_model(data_path: str, input_chunk_length: int, output_chunk_length: int):
#     """
#     Train the NBEATS model with covariates.
#     """
#     # Load the data and covariates
#     series, covariates = load_data(data_path)

#     # Split data into training and validation sets
#     train_series, val_series = series.split_after(0.8)
#     train_covariates, val_covariates = covariates.split_after(0.8)

#     # Create the model
#     model = create_model(input_chunk_length, output_chunk_length)

#     # Fit the model with covariates
#     print("Training the model...")
#     model.fit(series=train_series, past_covariates=train_covariates)

#     # Evaluate the model
#     forecast = model.predict(n=output_chunk_length, series=val_series, past_covariates=val_covariates)
#     print("Forecast complete.")

#     return model, forecast


# if __name__ == "__main__":
#     data_path = "data/energy_data.csv"  # Path to your dataset
#     input_chunk_length = 24  # Number of past hours for input
#     output_chunk_length = 12  # Number of future hours to predict

#     model, forecast = train_model(data_path, input_chunk_length, output_chunk_length)

#     # You can now plot the forecast
#     forecast.plot(label="Forecast")
