import plotly.express as px
from datetime import datetime
import streamlit as st
from constants.generic import LUFTDATEN_DAILY_AGG_TABLE, NOE_MAP_CENTER
from utils.db import get_db
from utils.dto import FilterConfig


def animate_map(config: FilterConfig, animate_speed: int = 250):
    """
    Animate the map for the given sensor and time range.

    Args:
        sensor (str): The sensor to animate.
        start_date (datetime): The start date for the animation.
        end_date (datetime): The end date for the animation.
    """
    
    sensor = config.selected_sensor
    start_date = config.start_date
    end_date = config.end_date
    
    qry = f"""
    SELECT Datetime, Station, Latitude as lat, Longitude as lon, {sensor} FROM {LUFTDATEN_DAILY_AGG_TABLE}
    WHERE Datetime >= %(start_date)s
    AND Datetime <= %(end_date)s
    AND {sensor} IS NOT NULL
    """
    df = get_db().query_df(qry, { "start_date": start_date, "end_date": end_date })
    
    df["Datum"] = df["Datetime"].dt.strftime("%d.%m.%y")
    df["Längengrad"] = df["lat"]
    df["Breitengrad"] = df["lon"]
    df[config.human_readable_sensor] = df[sensor].astype(float).round(2)
    
    center = {"lat": NOE_MAP_CENTER[0], "lon": NOE_MAP_CENTER[1]}
    
    fig = px.scatter_mapbox(
        df,
        lat="Längengrad",
        lon="Breitengrad",
        color=sensor,
        color_discrete_sequence=["blue"],
        hover_name="Station",
        height=600,
        width=800,
        hover_data=["Station", config.human_readable_sensor],
        color_continuous_scale=px.colors.sequential.Bluered,
        zoom=7,
        # range_color=[min_sensor, max_sensor],
        animation_frame="Datum",
        animation_group="Station",
        title=f"Tagesmittelwerte {config.human_readable_sensor} über das Jahr {config.target_year}"
    )
    
    fig.update_traces(marker=dict(size=14))
    
    
    fig.update_layout(
        updatemenus=[{
                "buttons": [
                    {
                        "args": [None, {"frame": {"duration": animate_speed, "redraw": True}, "fromcurrent": True}],
                        "label": "Start",
                        "method": "animate",
                    },
                    {
                        "args": [[None], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate", "transition": {"duration": 0}}],
                        "label": "Stop",
                        "method": "animate",
                    },
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 87},
                "showactive": False,
                "type": "buttons",
                "x": 0.1,
                "xanchor": "right",
                "y": 0,
                "yanchor": "top",
        }],
        mapbox_style="carto-positron",
        mapbox=dict(
            center=center
        ),
        margin=dict(l=0, r=0, t=50, b=0)
    )
    
    return fig