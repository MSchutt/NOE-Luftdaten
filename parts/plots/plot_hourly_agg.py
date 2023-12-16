
import plotly.express as px

from utils.dto import FilterConfig
from utils.filter import hourly_aggregate
from typing import Tuple, List


def get_hourly_plot(filter: FilterConfig, annotations: List[Tuple[int, str]] = None):
    if annotations is None:
        annotations = []
    
    df = hourly_aggregate(filter)
    
    fig = px.line(df, x="Datetime", y=filter.selected_sensor, color="Station", title=f"Stundenmittelwerte für {filter.human_readable_sensor}")
    
    fig.update_layout(
        xaxis_title="Datum",
        yaxis_title=filter.human_readable_sensor,
        legend_title="Station"
    )
    
    if len(annotations) > 0:
        for y, name, color in annotations:
            fig.add_hline(y=y, line_dash="dash", line_width=1, line_color=color, showlegend=True, name=name)
    
    return fig