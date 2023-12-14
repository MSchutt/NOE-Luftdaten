import pandas as pd
import streamlit as st

def calculate_and_plot_indices(df: pd.DataFrame, selected_stations, selected_sensor, human_readable_sensor) -> pd.DataFrame:
    """
    Calculate the indezes of NO2, O3, PM10 or PM2_5 of a DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame.
        selected_stations: Stations selected in starter.py
        selected_sensor: Sensor selected in starter.py
        human_readable_sensor: Human Readable name of the sensor

    Returns:
        No return.
    """
    # limits plus labels
    limits = {'NO2': [0, 40, 90, 120, 230, 340, 1000],
              'O3': [0, 50, 100, 130, 240, 380, 800],
              'PM10': [0, 10, 20, 25, 50, 75, 800],
              'PM2_5': [0, 20, 40, 50, 100, 150, 1200]
              }
    labels = ['very good', 'good', 'medium', 'poor', 'very poor', 'extremely poor']

    df = df.drop(['Datetime_End', 'Longitude', 'Latitude', 'Altitude', 'G', 'T', 'Wind_u', 'Wind_v'])

    for i in selected_stations:
        # Use only the 25 last rows because of rolling mean
        station = df[df['Station'] == i][-25:]
        if selected_sensor == 'PM10' or selected_sensor == 'PM2_5':
            # Calculate rolling mean of the last 24 rows
            station['rolling'] = station[selected_sensor].rolling(24).mean()

            station[selected_sensor] = pd.cut(station['rolling'], bins = limits[selected_sensor], labels=labels)

            station = station.drop('rolling')

            # Plot indices for last hour
            st.metric(label=f"Europäischer Luftqualitätsindex für {human_readable_sensor}", value=station[selected_sensor][-1])

        else:
            # Create bins which contain the different labels
            station[selected_sensor] = pd.cut(station[selected_sensor], bins = limits[selected_sensor], labels=labels)

            # Plot indices for last hour
            st.metric(label=f"Europäischer Luftqualitätsindex für {human_readable_sensor}", value=station[selected_sensor][-1])


