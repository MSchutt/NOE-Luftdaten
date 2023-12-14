
import pandas as pd
from datetime import datetime
from typing import List, Dict
import streamlit as st
import plotly.express as px
from utils.dto import FilterConfig
from utils.filter import get_per_year_averages
import plotly.express as px


def get_per_year_avg_plot(config: FilterConfig) -> pd.DataFrame:
    df = get_per_year_averages(config)
    
    fig = px.bar(df, x="year", y="avg", color="Station", title=f"Jahresmittelwerte für {config.human_readable_sensor}", barmode="group")
    fig.add_hline(y=config.global_average, line_dash="dash", line_width=3, line_color="orange", showlegend=True, name="⌀ Jahr alle Stationen")
    fig.update_layout(
        xaxis_title="Jahr",
        yaxis_title=config.human_readable_sensor,
        legend_title="Station"
    )

    return st.plotly_chart(fig, use_container_width=True)
    
    
    