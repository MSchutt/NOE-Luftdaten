import pandas as pd
import streamlit as st
from typing import Tuple, Dict, List
from datetime import datetime
import pytz

from constants.generic import DEFAULT_END_DATE, DEFAULT_SENSOR, DEFAULT_START_DATE, DEFAULT_STATION, MAX_STATIONS_SELECT


def get_filter_header(min_date: datetime, max_date: datetime, possible_stations: List[str], possible_sensors: Dict[str, str]) -> Tuple[datetime, datetime, List[str], str]:
    """
    Returns the filter header for the data filtering section.

    Args:
        min_date (datetime): The minimum date for the date range slider.
        max_date (datetime): The maximum date for the date range slider.
        possible_stations (List[str]): The list of possible station names.
        possible_sensors (Dict[str, str]): The dictionary of possible sensor names and their corresponding labels.

    Returns:
        Tuple[datetime, datetime, List[str], str]: A tuple containing the start date, end date, selected stations, and selected sensor.
    """
    result = get_daterange_slider("Datum", min_date, max_date)
    # Only 1 date selected
    if len(result) == 1:
        start_date = result[0]
        end_date = None
    elif len(result) == 2:
        start_date, end_date = result
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_station = st.multiselect(
            "Station",
            possible_stations,
            max_selections=MAX_STATIONS_SELECT,
            default=DEFAULT_STATION
        )
    
    with col2:
        selected_sensor = st.selectbox("Sensor", list(possible_sensors.keys()), index=2, format_func=lambda x: possible_sensors[x])
        
        
    return (start_date, end_date, selected_station, selected_sensor)
    

def get_daterange_slider(label: str, min_date: datetime, max_date: datetime) -> Tuple[datetime, datetime]:
    """
    Returns a date range slider widget.

    Args:
        label (str): The label of the slider.
        min_date (datetime): The minimum date value for the slider.
        max_date (datetime): The maximum date value for the slider.

    Returns:
        Streamlit Slider Element
    """
    
    return st.date_input(
        label,
        (min_date.replace(tzinfo=None), max_date.replace(tzinfo=None)),
        min_date,
        max_date,
        format="DD.MM.YYYY"
    )
    
    return st.slider(
        label,
        min_value=min_date.replace(tzinfo=None),
        max_value=max_date.replace(tzinfo=None),
        value=(DEFAULT_START_DATE.replace(tzinfo=None), DEFAULT_END_DATE.replace(tzinfo=None))
    )