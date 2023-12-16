import pandas as pd
from datetime import timedelta
import streamlit as st

from utils.dto import FilterConfig
from utils.filter import hourly_aggregate
from utils.mapper import format_timestamp

# Limits plus labels
LIMITS = {'NO2': [0, 40, 90, 120, 230, 340, 1000],
            'O3': [0, 50, 100, 130, 240, 380, 800],
            'PM10': [0, 10, 20, 25, 50, 75, 800],
            'PM2_5': [0, 20, 40, 50, 100, 150, 1200]
            }
LABELS = ['Sehr Gut', 'Gut', 'Mittel', 'Schlecht', 'Sehr Schlecht', 'Extrem Schlecht']

# Recommendations of the European Environment Agency based on the European Air Quality Index
RECOMMENDATIONS = {'Sehr Gut': 'Die Luftqualität ist sehr gut. Genießen Sie ihre üblichen Aktivitäten im Freien.',
                   'Gut': 'Genießen Sie ihre üblichen Aktivitäten im Freien.',
                   'Mittel': 'Genießen Sie ihre üblichen Aktivitäten im Freien.',
                   'Schlecht': 'Erwägen Sie, intensive Aktivitäten im Freien zu reduzieren, wenn Sie Symptome wie Augenschmerzen, Husten oder Halsschmerzen bemerken.',
                   'Sehr schlecht': 'Erwägen Sie, intensive Aktivitäten im Freien zu reduzieren, wenn Sie Symptome wie Augenschmerzen, Husten oder Halsschmerzen bemerken.',
                   'Extrem schlect': 'Reduzieren Sie körperliche Aktivitäten im Freien.'}
RECOMMENDATIONS_SENSITIVE = {'Sehr Gut': 'Die Luftqualität ist sehr gut. Genießen Sie ihre üblichen Aktivitäten im Freien.',
                   'Gut': 'Genießen Sie ihre üblichen Aktivitäten im Freien.',
                   'Mittel': 'Erwägen Sie, intensive Aktivitäten im Freien zu reduzieren, wenn Sie Symptome bemerken.',
                   'Schlecht': 'Erwägen Sie eine Reduzierung der körperlichen Aktivitäten, insbesondere im Freien, insbesondere wenn Sie Symptome bemerken.',
                   'Sehr schlecht': 'Reduzieren Sie körperliche Aktivitäten, insbesondere im Freien, insbesondere wenn Sie Symptome bemerken.',
                   'Extrem schlect': 'Vermeiden Sie körperliche Aktivitäten im Freien.'}

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
    
    df = hourly_aggregate(config).set_index("Datetime")
    
    fmt_start_date = format_timestamp(start_date)
    fmt_end_date = format_timestamp(end_date)
        
    selected_sensor = config.selected_sensor

    for selected_station in config.selected_stations:
        # Use the 25 first and last rows for comparison
        # 25 rows needed for rolling mean
        index_start_date = df[df['Station'] == selected_station][:25]
        index_end_date = df[df['Station'] == selected_station][-25:]

        # Check if that is no missing values and sensor is one of the sensors for which the index can be calculated
        if index_start_date[selected_sensor].isna().sum() == 0 and index_end_date[selected_sensor].isna().sum() == 0 and selected_sensor in LIMITS.keys():

            if selected_sensor == 'PM10' or selected_sensor == 'PM2_5':
                # Calculate rolling mean
                index_start_date['rolling'] = index_start_date[selected_sensor].rolling(24).mean()
                index_end_date['rolling'] = index_end_date[selected_sensor].rolling(24).mean()

                # Get the labels for the sensor values
                index_start_date[selected_sensor] = pd.cut(index_start_date['rolling'], bins = LIMITS[selected_sensor], labels=LABELS)
                index_end_date[selected_sensor] = pd.cut(index_end_date['rolling'], bins = LIMITS[selected_sensor], labels=LABELS)

                # Plot indices for last hour
                st.metric(label=f"Europäischer Luftqualitätsindex in {selected_station} für {config.human_readable_sensor} ({fmt_start_date} - {fmt_end_date})", value=index_end_date[selected_sensor][-1], delta = index_start_date[selected_sensor][-1])                

                # Markdown with recommendations
                st.markdown('''***Verhaltensempfehlung für die allgemeine Bevölkerung***:''')
                st.markdown(RECOMMENDATIONS[index_end_date[selected_sensor][-1]])

                st.markdown('''***Verhaltensempfehlung für die sensible Bevölkerung***:''')
                st.markdown(RECOMMENDATIONS_SENSITIVE[index_end_date[selected_sensor][-1]])


            else:
                # Get the labels for the sensor values
                index_start_date[selected_sensor] = pd.cut(index_start_date[selected_sensor], bins = LIMITS[selected_sensor], labels=LABELS)
                index_end_date[selected_sensor] = pd.cut(index_end_date[selected_sensor], bins = LIMITS[selected_sensor], labels=LABELS)

                # Plot indices for last hour
                st.metric(label=f"Europäischer Luftqualitätsindex in {selected_station} für {config.human_readable_sensor} ({fmt_start_date} - {fmt_end_date})", value= index_end_date[selected_sensor][-1], delta = index_start_date[selected_sensor][-1])

                # Markdown with recommendations
                st.markdown('''***Verhaltensempfehlung für die allgemeine Bevölkerung***:''')
                st.markdown(RECOMMENDATIONS[index_end_date[selected_sensor][-1]])

                st.markdown('''***Verhaltensempfehlung für die sensible Bevölkerung***:''')
                st.markdown(RECOMMENDATIONS_SENSITIVE[index_end_date[selected_sensor][-1]])

        # If index can't be calculated for this sensor or there is missing values
        else:
            st.metric(label=f"Nicht verfügbar: Europäischer Luftqualitätsindex in {selected_station} für {config.human_readable_sensor} ({fmt_start_date} - {fmt_end_date})", value='-')

