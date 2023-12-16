
import plotly.express as px

from utils.dto import FilterConfig
from utils.filter import daily_aggregate
from typing import Tuple, List


def get_daily_plot(filter: FilterConfig, annotations: List[Tuple[int, str]] = None):
    if annotations is None:
        annotations = []
    
    df = daily_aggregate(filter)
    
    fig = px.line(df, x="Datetime", y=filter.selected_sensor, color="Station", title=f"Tagesmittelwerte für {filter.human_readable_sensor}")
    
    if len(annotations) > 0:
        for y, name, color in annotations:
            fig.add_hline(y=y, line_dash="dash", line_width=1, line_color=color, showlegend=True, name=name)
    
    return fig