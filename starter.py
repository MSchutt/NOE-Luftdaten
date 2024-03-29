import streamlit as st
from constants.sensor import POSSIBLE_SENSOR_MAP
from parts.filter_header import get_filter_header
from parts.map import get_map
from parts.plots.daily_avg import get_daily_chart
from parts.plots.monthly_avg import get_monthly_averages_plot
from parts.plots.yearly_avg import get_per_year_avg_plot
from utils.dto import FilterConfig
from utils.filter import get_global_sensor_averages
from utils.generic import db_get_daterange, db_get_stations
from utils.air_quality_indeces import calculate_and_plot_indices

st.set_page_config(
    page_title="NÖ Luftgüte",
    page_icon="💨"
)


st.title("Niederösterreich - Luftgüte - Übersicht")

st.write("In dieser Ansicht können Tages-, Monats- und Jahresmittelwerte betrachtet werden. Es besteht die Möglichkeit, einen zeitlichen Filter einzustellen, eine oder mehrere Stationen auszuwählen und nach Sensortypen (zum Beispiel Temperatur) zu filtern.")

min_date, max_date = db_get_daterange()
possible_stations = db_get_stations()

start_date, end_date, selected_stations, selected_sensor = get_filter_header(min_date, max_date, possible_stations, POSSIBLE_SENSOR_MAP)

if start_date is None or end_date is None:
    st.stop()

# time diff between start and end date
diff = end_date - start_date
if diff.days < 730:
    st.error("Der ausgewählte Zeitraum muss mindestens 730 Tage (2 Jahr) betragen.")
    st.stop()

# Apply the filter
global_sensor_average = get_global_sensor_averages(start_date, end_date)
filter_config = FilterConfig(
    start_date=start_date,
    end_date=end_date,
    global_average=global_sensor_average.get(selected_sensor),
    selected_stations=selected_stations,
    selected_sensor=selected_sensor,
    human_readable_sensor=POSSIBLE_SENSOR_MAP.get(selected_sensor),
    target_year=end_date.year
)


st.markdown("""---""")

# Map Selection returns all sort of options (clicked market, etc.) -> maybe we want to do something with that later?
# map_selection = get_map(filter_config)
map_selection = get_map(filter_config)

# Daily Plot
get_daily_chart(filter_config)

# Per Month Plot
get_monthly_averages_plot(filter_config)

# Per Year Plot
get_per_year_avg_plot(filter_config)

# Plot Air Quality Index of last hour
calculate_and_plot_indices(filter_config)

