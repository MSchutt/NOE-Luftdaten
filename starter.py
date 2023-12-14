import streamlit as st
from constants.generic import DATETIME_COLUMN, MEAN_COLUMN_NAME
from constants.sensor import POSSIBLE_SENSOR_MAP
from parts.filter_header import get_filter_header
from parts.map import get_map
from utils.filter import apply_time_station_filter, extract_station_coordinates
from utils.generic import db_get_daterange, db_get_stations


st.title("Niederösterreich - Luftgüte")

min_date, max_date = db_get_daterange()
possible_stations = db_get_stations()


start_date, end_date, selected_stations, selected_sensor = get_filter_header(min_date, max_date, possible_stations, POSSIBLE_SENSOR_MAP)
target_year = end_date.year


# Apply the filter
df = apply_time_station_filter(start_date, end_date, selected_stations, selected_sensor)
# yearly_agg = calculate_yearly_aggregate(df)

station_coordinates = extract_station_coordinates(df, lat_col="Latitude", lon_col="Longitude", station_col="Station", altitude_col="Altitude")

if len(df) == 0 or df[selected_sensor].isna().all():
    st.warning("Keine Daten gefunden - bitte Filter anpassen!")

st.markdown("""---""")

# Map Selection returns all sort of options (clicked market, etc.) -> maybe we want to do something with that later?
map_selection = get_map(station_coordinates)

# Plot the line chart, create an individual line for each station
tabs = st.tabs(selected_stations)

st.write(df.head(10))

# Generic plot
for i, tab in enumerate(tabs):
    with tab:
        df_station = df[df["Station"] == selected_stations[i]].copy()
        df_station[MEAN_COLUMN_NAME] = df_station[selected_sensor].mean()
        
        if len(df_station) == 0 or df_station[selected_sensor].isna().all():
            st.warning("Keine Daten gefunden - an dieser Station ist dieser Sensor leider nicht verbaut.")
        else:
            st.line_chart(
                df_station,
                x=DATETIME_COLUMN,
                y=[selected_sensor, MEAN_COLUMN_NAME]
            )