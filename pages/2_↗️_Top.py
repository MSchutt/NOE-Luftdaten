import streamlit as st
from datetime import datetime
from constants.generic import AGGREGATION_LEVELS_TABLES, LUFTDATEN_DAILY_AGG_TABLE, LUFTDATEN_HOURLY_AGG_TABLE, LUFTDATEN_TABLE
from constants.sensor import POSSIBLE_SENSOR_MAP
from parts.filter_header import get_daterange_slider
from parts.map import get_map
from parts.plots.animation import animate_map
from parts.plots.daily_avg import get_daily_chart
from parts.plots.plot_hourly_agg import get_hourly_plot
from utils.db import get_db
from utils.dto import FilterConfig
from utils.filter import get_global_sensor_averages


st.title("Niederösterreich - Luftgüte - Best and Worst")

sensor = st.selectbox("Sensor", list(POSSIBLE_SENSOR_MAP.keys()), index=2, format_func=lambda x: POSSIBLE_SENSOR_MAP[x])
human_readable_sensor = POSSIBLE_SENSOR_MAP.get(sensor)


result = get_daterange_slider("Datum", datetime(2013, 1, 1), datetime(2022, 12, 31))
# Only 1 date selected
if len(result) == 1:
    start_date = result[0]
    end_date = None
elif len(result) == 2:
    start_date, end_date = result
    
if start_date is None or end_date is None:
    st.stop()
    
global_sensor_average = get_global_sensor_averages(start_date, end_date)
    
qry = f"""
SELECT * FROM (
    (SELECT Station, avg({sensor}) as {sensor} from {LUFTDATEN_DAILY_AGG_TABLE}
    WHERE Datetime >= %(start_date)s
    AND Datetime <= %(end_date)s
    GROUP BY Station
    ORDER BY {sensor} DESC
    LIMIT 3)
    UNION ALL
    (SELECT Station, avg({sensor}) as {sensor} from {LUFTDATEN_DAILY_AGG_TABLE}
    WHERE Datetime >= %(start_date)s
    AND Datetime <= %(end_date)s
    GROUP BY Station
    ORDER BY {sensor} ASC
    LIMIT 3)
) ORDER BY {sensor} ASC
    """

df = get_db().query_df(qry, { "start_date": start_date, "end_date": end_date })

df_cp = df.copy()
df_cp[human_readable_sensor] = df_cp[sensor]

df_cp = df_cp.drop(columns=[sensor])
select_col_name = "Details"
df_cp[select_col_name] = 0
all_cols = df_cp.columns
edited_df = st.data_editor(
    df_cp,
    hide_index=True,
    column_config={select_col_name: st.column_config.CheckboxColumn(required=True)},
    disabled=all_cols.drop(select_col_name).tolist(),
    use_container_width=True
)

filter_df = edited_df[edited_df[select_col_name] == 1]

if len(filter_df) > 0:

    selected_stations = filter_df["Station"].unique().tolist()

    if len(selected_stations) > 0:
        filter_config = FilterConfig(
            start_date=start_date,
            end_date=end_date,
            global_average=global_sensor_average.get(sensor),
            selected_stations=selected_stations,
            selected_sensor=sensor,
            human_readable_sensor=POSSIBLE_SENSOR_MAP.get(sensor),
            target_year=end_date.year
        )
        get_daily_chart(filter_config)
        
        
        get_map(filter_config)