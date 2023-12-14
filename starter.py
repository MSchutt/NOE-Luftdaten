import streamlit as st
from constants.generic import DATETIME_COLUMN, LUFTDATEN_DAILY_AGG_TABLE, LUFTDATEN_HOURLY_AGG_TABLE, LUFTDATEN_MONTHLY_AGG_TABLE, LUFTDATEN_WEEKLY_AGG_TABLE, LUFTDATEN_YEARLY_AGG_TABLE, MEAN_COLUMN_NAME
from constants.sensor import POSSIBLE_SENSOR_MAP
from parts.filter_header import get_filter_header
from parts.map import get_map
from parts.plots.generic import get_generic_line_chart
from utils.filter import apply_time_station_filter, extract_station_coordinates, get_global_sensor_averages
from utils.generic import db_get_daterange, db_get_stations
from utils.air_quality_indeces import calculate_and_plot_indices

st.title("Niederösterreich - Luftgüte")

min_date, max_date = db_get_daterange()
possible_stations = db_get_stations()


start_date, end_date, selected_stations, selected_sensor = get_filter_header(min_date, max_date, possible_stations, POSSIBLE_SENSOR_MAP)
target_year = end_date.year


# Apply the filter
hourly_df = apply_time_station_filter(start_date, end_date, selected_stations, selected_sensor, table_name=LUFTDATEN_HOURLY_AGG_TABLE)
daily_df = apply_time_station_filter(start_date, end_date, selected_stations, selected_sensor, table_name=LUFTDATEN_DAILY_AGG_TABLE)
weekly_df = apply_time_station_filter(start_date, end_date, selected_stations, selected_sensor, table_name=LUFTDATEN_WEEKLY_AGG_TABLE)
monthly_df = apply_time_station_filter(start_date, end_date, selected_stations, selected_sensor, table_name=LUFTDATEN_MONTHLY_AGG_TABLE)
yearly_df = apply_time_station_filter(start_date, end_date, selected_stations, selected_sensor, table_name=LUFTDATEN_YEARLY_AGG_TABLE)

human_readable_sensor = POSSIBLE_SENSOR_MAP.get(selected_sensor)

global_sensor_average = get_global_sensor_averages(start_date, end_date)

station_coordinates = extract_station_coordinates(daily_df, lat_col="Latitude", lon_col="Longitude", station_col="Station", altitude_col="Altitude")

if len(daily_df) == 0 or daily_df[selected_sensor].isna().all():
    st.warning("Keine Daten gefunden - bitte Filter anpassen!")
else:
    st.markdown("""---""")

    # Map Selection returns all sort of options (clicked market, etc.) -> maybe we want to do something with that later?
    map_selection = get_map(station_coordinates)

    # Plot the line chart, create an individual line for each station
    st.plotly_chart(get_generic_line_chart(daily_df, selected_sensor, global_sensor_average, title=f"Tagesdurchschnitt für {human_readable_sensor}"))
    st.plotly_chart(get_generic_line_chart(weekly_df, selected_sensor, global_sensor_average, title=f"Wochendurchschnitt für {human_readable_sensor}"))
    st.plotly_chart(get_generic_line_chart(monthly_df, selected_sensor, global_sensor_average, title=f"Monatsdurchschnitt für {human_readable_sensor}"))
    st.plotly_chart(get_generic_line_chart(yearly_df, selected_sensor, global_sensor_average, title=f"Jahresdurchschnitt für {human_readable_sensor}"))
    
    # Plot Air Quality Index of last hour
    calculate_and_plot_indices(hourly_df, selected_stations, selected_sensor, human_readable_sensor)