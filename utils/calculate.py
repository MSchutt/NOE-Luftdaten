import pandas as pd

from constants.generic import DATETIME_COLUMN

def calculate_yearly_aggregate(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the yearly aggregate of a DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: The DataFrame with yearly aggregated data.
    """
    # Aggregate by Datetime_Start, station and month so that we get the data per month and station
    df = df.groupby([df[DATETIME_COLUMN].dt.month, "Station"]).mean().reset_index()
    return df
