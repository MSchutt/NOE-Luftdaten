import pandas as pd
import streamlit as st
from datetime import datetime
from typing import List, Union, Dict

from constants.generic import ALWAYS_KEEP_COLUMNS, LUFTDATEN_DAILY_AGG_TABLE, LUFTDATEN_TABLE, LUFTDATEN_YEARLY_AGG_TABLE
from utils.db import get_db
from utils.dto import FilterConfig


def daily_aggregate(config: FilterConfig) -> pd.DataFrame:
    """ Returns the daily aggregate for the given filter configuration.

    Args:
        config (FilterConfig): The filter configuration.

    Returns:
        pd.DataFrame: The DataFrame containing the daily aggregate.
    """    
    
    qry = f"""
    SELECT Station, Datetime, {config.selected_sensor} as {config.selected_sensor} FROM {LUFTDATEN_DAILY_AGG_TABLE}
    WHERE Datetime >= %(start_date)s
    AND Datetime <= %(end_date)s
    AND Station IN %(selected_stations)s
    """
    
    return get_db().query_df(qry, { "start_date": config.start_date, "end_date": config.end_date, "selected_stations": config.selected_stations })
    


def get_per_day_averages(config: FilterConfig) -> pd.DataFrame:
    """ Returns the per day averages for the given filter configuration.

    Args:
        config (FilterConfig): The filter configuration.

    Returns:
        pd.DataFrame: The DataFrame containing the per day averages.
    """    
    
    qry = f"""
    SELECT Station, Datetime, {config.selected_sensor} as {config.selected_sensor} FROM {LUFTDATEN_DAILY_AGG_TABLE}
    WHERE Datetime >= %(start_date)s
    AND Datetime <= %(end_date)s
    AND Station IN %(selected_stations)s
    ORDER BY Station, Datetime ASC
    """
    db = get_db()
    
    return db.query_df(qry, { "start_date": config.start_date, "end_date": config.end_date, "selected_stations": config.selected_stations })


def get_per_year_averages(config: FilterConfig) -> pd.DataFrame:
    """
    Get the averages from the database for the given time range.

    Args:
        config (FilterConfig): The filter configuration.

    Returns:
        pd.DataFrame: The DataFrame containing the averages.
    """
    qry = f"""
    SELECT Station, YEAR(Datetime_Start) as year, avg({config.selected_sensor}) as avg FROM {LUFTDATEN_TABLE}
    WHERE Station IN %(selected_stations)s
    GROUP BY Station, YEAR(Datetime_Start)
    ORDER BY Station, YEAR(Datetime_Start) ASC
    """
    
    db = get_db()
    
    df = db.query_df(qry, { "selected_stations": config.selected_stations, "start_date": config.start_date, "end_date": config.end_date })
    
    return df

def get_monthly_averages(start_date: datetime, end_date: datetime, selected_stations: List[str], selected_sensor: str) -> pd.DataFrame:
    """ Returns the per month aggregated values for the given time range and selected stations.

    Args:
        start_date (datetime): start date
        end_date (datetime): end date
        selected_stations (List[str]): selected stations
        selected_sensor (str): selected sensor

    Returns:
        pd.DataFrame: The DataFrame containing the monthly aggregated avlues.
    """    
    
    db = get_db()
    
    qry = f"""
    SELECT Station, Longitude, Latitude, Altitude, month(Datetime_Start) as month, avg({selected_sensor}) as {selected_sensor} FROM {LUFTDATEN_TABLE}
    WHERE Datetime_Start >= %(start_date)s
    AND Datetime_Start <= %(end_date)s
    AND Station IN %(selected_stations)s
    GROUP BY Station, Longitude, Latitude, Altitude, month(Datetime_Start)
    ORDER BY Station, month(Datetime_Start) ASC
    """
    
    return db.query_df(qry, { "start_date": start_date, "end_date": end_date, "selected_stations": selected_stations, "selected_sensor": selected_sensor })


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
    

def load_station_coordinates(config: FilterConfig) -> pd.DataFrame:
    """ Loads the station coordinates for the given filter configuration.

    Args:
        config (FilterConfig): The filter configuration.

    Returns:
        pd.DataFrame: The DataFrame containing the station coordinates.
    """
    db = get_db()
    
    df = db.query_df(f"SELECT Station, Longitude, Latitude, Altitude FROM {LUFTDATEN_TABLE} WHERE Station IN %(selected_stations)s", { "selected_stations": config.selected_stations })
    
    df["info"] = df.apply(lambda row: f"{row['Station']} ({int(row['Altitude'])}m)", axis=1)
    
    return df