import streamlit as st
from constants.generic import DATETIME_COLUMN, MEAN_COLUMN_NAME
from constants.sensor import POSSIBLE_SENSOR_MAP
from parts.filter_header import get_filter_header
from parts.map import get_map
from parts.plots.generic import get_generic_line_chart
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
st.plotly_chart(get_generic_line_chart(df, selected_sensor))