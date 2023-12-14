import pandas as pd
from typing import Dict
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from utils.dto import FilterConfig
from utils.filter import get_per_day_averages


def get_daily_chart(config: FilterConfig):
    """
    Generate a line chart for a selected sensor from a DataFrame.

    Args:
        config (FilterConfig): The filter configuration.

    Returns:
        The line chart widget.
    """
    
    df = get_per_day_averages(config)
    
    # x axis -> Datetime
    # y axis -> selected_sensor
    # color = Station
    # Also add average
    # plot global average as well
    fig = px.line(df, x="Datetime", y=config.selected_sensor, color="Station", title=f"Tagesmittelwerte für {config.human_readable_sensor}")
    fig.add_hline(y=config.global_average, line_dash="dash", line_width=3, line_color="orange", showlegend=True, name="⌀ Jahr alle Stationen")
    
    
    fig.update_layout(
        xaxis_title="Datum",
        yaxis_title=config.human_readable_sensor,
        legend_title="Station"
    )
    
    return st.plotly_chart(fig)
