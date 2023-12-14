import pandas as pd
from datetime import timedelta
import streamlit as st

from utils.dto import FilterConfig
from utils.filter import daily_aggregate
from utils.mapper import format_timestamp

# limits plus labels
LIMITS = {'NO2': [0, 40, 90, 120, 230, 340, 1000],
            'O3': [0, 50, 100, 130, 240, 380, 800],
            'PM10': [0, 10, 20, 25, 50, 75, 800],
            'PM2_5': [0, 20, 40, 50, 100, 150, 1200]
            }
LABELS = ['Sehr Gut', 'Gut', 'Mittel', 'Schlecht', 'Sehr Schlecht', 'Extrem Schlecht']

def calculate_and_plot_indices(config: FilterConfig) -> None:
    """
    Calculate the indezes of NO2, O3, PM10 or PM2_5 of a DataFrame.

    Args:
        config (FilterConfig): The filter config.
    """
    # Only requires the rolling window of the last 24 days.
    end_date = config.end_date
    start_date = end_date - timedelta(days=60)
    config.start_date = start_date
    
    df = daily_aggregate(config).set_index("Datetime")
    
    fmt_start_date = format_timestamp(start_date)
    fmt_end_date = format_timestamp(end_date)
        
    selected_sensor = config.selected_sensor

    for selected_station in config.selected_stations:
        # Use only the 25 last rows because of rolling mean
        station = df[df['Station'] == selected_station][-25:]
        if selected_sensor == 'PM10' or selected_sensor == 'PM2_5':
            # Calculate rolling mean of the last 24 rows
            station['rolling'] = station[selected_sensor].rolling(24).mean()

            station[selected_sensor] = pd.cut(station['rolling'], bins = LIMITS[selected_sensor], labels=LABELS)

            station = station.drop('rolling')

            # Plot indices for last hour
            st.metric(label=f"Europäischer Luftqualitätsindex für {config.human_readable_sensor} ({fmt_start_date} - {fmt_end_date})", value=station[selected_sensor][-1])

        else:
            # Create bins which contain the different labels
            station[selected_sensor] = pd.cut(station[selected_sensor], bins = LIMITS[selected_sensor], labels=LABELS)

            # Plot indices for last hour
            st.metric(label=f"Europäischer Luftqualitätsindex für {config.human_readable_sensor} ({fmt_start_date} - {fmt_end_date})", value=station[selected_sensor][-1])


