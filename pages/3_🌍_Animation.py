import streamlit as st
from datetime import datetime
from constants.sensor import POSSIBLE_SENSOR_MAP
from parts.plots.animation import animate_map
from utils.dto import FilterConfig

st.title("Niederösterreich - Luftgüte - Animation")

selected_sensor = st.selectbox("Sensor", list(POSSIBLE_SENSOR_MAP.keys()), index=2, format_func=lambda x: POSSIBLE_SENSOR_MAP[x])
year = st.slider("Jahr", 2013, 2022, 2022)
animation_speed = st.slider("Animationsgeschwindigkeit (ms)", 100, 1000, 250)

human_readable_sensor = POSSIBLE_SENSOR_MAP.get(selected_sensor)

start_date = datetime(year, 1, 1)
end_date = datetime(year, 12, 31)

config = FilterConfig(
    start_date=start_date,
    end_date=end_date,
    global_average=None,
    selected_stations=None,
    selected_sensor=selected_sensor,
    human_readable_sensor=human_readable_sensor,
    target_year=year
)

st.plotly_chart(animate_map(config, animation_speed), use_container_width=True)