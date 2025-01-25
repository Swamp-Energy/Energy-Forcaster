from prophet import Prophet
import pandas as pd

# Define the forecasting model
def create_forecast_model(data):
    """
    Train a Prophet model on the provided data.

    Args:
        data (DataFrame): A pandas DataFrame with 'ds' (datetime) and 'y' (target variable).
    
    Returns:
        model (Prophet): Trained Prophet model.
    """
    model = Prophet()
    model.fit(data)
    return model

def make_predictions(model, future_periods, frequency='H'):
    """
    Use the trained model to make future predictions.

    Args:
        model (Prophet): A trained Prophet model.
        future_periods (int): Number of periods to predict.
        frequency (str): Frequency of predictions (e.g., 'H' for hourly, 'D' for daily).

    Returns:
        DataFrame: Forecast with predictions and confidence intervals.
    """
    future = model.make_future_dataframe(periods=future_periods, freq=frequency)
    forecast = model.predict(future)
    return forecast
