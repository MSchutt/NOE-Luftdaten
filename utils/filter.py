import pandas as pd
import streamlit as st
from datetime import datetime
from typing import List, Union, Dict

from constants.generic import ALWAYS_KEEP_COLUMNS, LUFTDATEN_DAILY_AGG_TABLE, LUFTDATEN_TABLE
from utils.db import get_db


@st.cache_data
def get_global_sensor_averages(start_date: datetime, end_date: datetime) -> Dict[str, float]:
    """
    Get the averages from the database for the given time range.

    Args:
        start_date (datetime): The start date for the filter.
        end_date (datetime): The end date for the filter.

    Returns:
        pd.DataFrame: The DataFrame containing the averages.
    """
    qry = f"""
    SELECT avg(G) as G_avg, avg(NO) as NO_avg, avg(NO2) as NO2_avg, avg(O3) as O3_avg, avg(PM10) as PM10_avg, avg(PM2_5) as PM2_5_avg, avg(T) as T_avg FROM {LUFTDATEN_TABLE}
    WHERE Datetime_Start >= %(start_date)s
    AND Datetime_Start <= %(end_date)s
    """
    
    db = get_db()

    df = db.query_df(qry, { "start_date": start_date, "end_date": end_date })
    
    return {
        "G": df["G_avg"].iloc[0],
        "NO": df["NO_avg"].iloc[0],
        "NO2": df["NO2_avg"].iloc[0],
        "O3": df["O3_avg"].iloc[0],
        "PM10": df["PM10_avg"].iloc[0],
        "PM2_5": df["PM2_5_avg"].iloc[0],
        "T": df["T_avg"].iloc[0],
    }

@st.cache_data
def apply_time_station_filter(start_date: datetime, end_date: datetime, selected_stations: List[str], selected_sensor: Union[List[str], str], table_name: str = LUFTDATEN_DAILY_AGG_TABLE) -> pd.DataFrame:
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
    target_cols = ",".join([*ALWAYS_KEEP_COLUMNS, *sensor_filter])
    
    qry = f"""
    SELECT {target_cols} FROM {table_name}
    WHERE Station IN %(selected_stations)s
    AND Datetime >= %(start_date)s
    AND Datetime <= %(end_date)s
    """
    
    db = get_db()
    
    df = db.query_df(qry, { "selected_stations": selected_stations, "start_date": start_date, "end_date": end_date, "target_cols": target_cols })
    
    return df
    


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