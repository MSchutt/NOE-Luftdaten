import pandas as pd
import streamlit as st
from datetime import datetime
from typing import List, Union

from constants.generic import ALWAYS_KEEP_COLUMNS

@st.cache_data
def apply_time_station_filter(df: pd.DataFrame, start_date: datetime, end_date: datetime, selected_stations: List[str], selected_sensor: Union[List[str], str]) -> pd.DataFrame:
    """
    Apply filters to a DataFrame based on start date, end date, and selected stations.

    Args:
        df (pd.DataFrame): The DataFrame to filter.
        start_date (datetime): The start date for the filter.
        end_date (datetime): The end date for the filter.
        selected_stations (List[str]): The list of selected stations for the filter.
        selected_sensor (Union[List[str], str]): The selected sensor for the filter.

    Returns:
        pd.DataFrame: The filtered DataFrame.
    """
    # We probably do not need this, but just in case we can pass a list of sensors, if we decide that we want to plot multiple sensors at once
    sensor_filter = selected_sensor if isinstance(selected_sensor, list) else [selected_sensor]
    target_cols = [*ALWAYS_KEEP_COLUMNS, *sensor_filter]
    
    filter_df = df[
        (df["Station"].isin(selected_stations)) &
        (df["Datetime_Start"] >= start_date) &
        (df["Datetime_End"] <= end_date)
    ]
    return filter_df[target_cols]
    


def extract_station_coordinates(df: pd.DataFrame, lat_col: str = "lat", lon_col: str = "lon", station_col: str = "Station", altitude_col: str = "Altitude"):
    """
    Extracts the station coordinates from a DataFrame and transforms the column names to "lat", "lon", and "info" (required format by streamlit).

    Args:
        df (pd.DataFrame): The DataFrame to extract the coordinates from.
        lat_col (str, optional): The column name for the latitude. Defaults to "lat".
        lon_col (str, optional): The column name for the longitude. Defaults to "lon".
        station_col (str, optional): The column name for the station name. Defaults to "Station".
        altitude_col (str, optional): The column name for the altitude. Defaults to "Altitude".

    Returns:
        pd.DataFrame: The DataFrame containing only the station coordinates.
    """
    filtered_df = df[[station_col, lat_col, lon_col, altitude_col]].drop_duplicates().reset_index(drop=True)
    
    # Create a info column which contains the station name and the altitude
    filtered_df["info"] = filtered_df.apply(lambda row: f"{row[station_col]} ({int(row[altitude_col])}m)", axis=1)

    
    return filtered_df[["info", lat_col, lon_col]].rename(columns={
        lon_col: "lon",
        lat_col: "lat"
    })