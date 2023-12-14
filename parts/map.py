import folium
from streamlit_folium import st_folium
from constants.generic import NOE_MAP_CENTER
from utils.dto import FilterConfig
import streamlit as st
from utils.filter import load_station_coordinates

def get_map(config: FilterConfig):
    """
    Generates a folium map with markers for each station in the given DataFrame.
    
    Returns:
        st_folium.Map: The folium map with markers.
    """
    
    df = load_station_coordinates(config)
    
    m = folium.Map(location=NOE_MAP_CENTER, zoom_start=8, tiles='CartoDB positron')
    for lat, lon, info in zip(df["Latitude"], df["Longitude"], df["info"]):
        folium.Marker(
            location=[lat, lon],
            popup=info
        ).add_to(m)
    return st_folium(m, use_container_width=True, height=400)