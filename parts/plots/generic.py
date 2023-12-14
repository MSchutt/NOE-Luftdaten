from typing import Dict
import pandas as pd
import plotly.express as px


def get_generic_line_chart(df: pd.DataFrame, selected_sensor: str, global_sensor_average: Dict[str, float], title: str = ""):
    """
    Generate a line chart for a selected sensor from a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing the sensor data.
        selected_sensor (str): The name of the sensor to plot.
        global_sensor_average (Dict[str, float]): The global average for each sensor.
        title (str, optional): The title of the chart. Defaults to "".

    Returns:
        The line chart widget.
    """
    
    average = global_sensor_average[selected_sensor]

    # x axis -> Datetime
    # y axis -> selected_sensor
    # color = Station
    # Also add average
    # plot global average as well
    fig = px.line(df, x="Datetime", y=selected_sensor, color="Station", title=title)
    fig.add_hline(y=average, line_dash="dash", line_width=3, line_color="orange")
    return fig
