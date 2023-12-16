import streamlit as st
import pandas as pd
from datetime import datetime
from constants.generic import LUFTDATEN_DAILY_AGG_TABLE, LUFTDATEN_HOURLY_AGG_TABLE
from constants.sensor import POSSIBLE_SENSOR_MAP

from parts.outlier.max_vals import get_aggregated_extreme_values
from parts.plots.plot_daily_agg import get_daily_plot
from parts.plots.plot_hourly_agg import get_hourly_plot
from utils.dto import FilterConfig
from utils.filter import get_global_sensor_averages
from utils.mapper import format_timestamp


st.title("Niederösterreich - Luftgüte")

# Dropdown select
selected_type = st.selectbox("Extremwert", ["Maximum", "Minimum"])
aggregate_type = st.selectbox("Aggregationsart", ["HMW (Stundenmittelwert)", "TMW (Tagesmittelwert)"])

use_min = bool(selected_type == "Minimum")

tbl = LUFTDATEN_HOURLY_AGG_TABLE if aggregate_type == "HMW (Stundenmittelwert)" else LUFTDATEN_DAILY_AGG_TABLE

year = st.slider("Jahr", 2013, 2022, 2022)
df = get_aggregated_extreme_values(year, use_min=use_min, table_name=tbl)

start_date = datetime(year, 1, 1)
end_date = datetime(year, 12, 31)

plt_func = get_hourly_plot if aggregate_type == "HMW (Stundenmittelwert)" else get_daily_plot

global_sensor_average = get_global_sensor_averages(start_date, end_date)

for row in df.to_dict("records"):
    sensor = row["max_col"]
    station = row["Station"]
    max_val = row[row["max_col"]]
    
    filter_config = FilterConfig(
        start_date=start_date,
        end_date=end_date,
        global_average=global_sensor_average.get(sensor),
        selected_stations=[station],
        selected_sensor=sensor,
        human_readable_sensor=POSSIBLE_SENSOR_MAP.get(sensor),
        target_year=end_date.year
    )
    
    annotations = [(max_val, f"{'Max' if not use_min else 'Min'} ({format_timestamp(row['Datetime'])}) = {max_val:.2f}", "orange")]
    df = plt_func(filter_config, annotations=annotations)
    
    st.plotly_chart(df, use_container_width=True)
    # get_daily_chart(filter_config)
