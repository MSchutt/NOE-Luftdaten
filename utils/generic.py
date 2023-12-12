import streamlit as st
import pandas as pd
from pathlib import Path


root_path = Path(__file__).parent.parent

# @TODO: Load data from ClickHouse

@st.cache_data
def get_data() -> pd.DataFrame:
    """ Loads the data from the data folder.

    Returns:
        pd.DataFrame: Preprocessed Dataframe
    """    
    return pd.read_feather(root_path / "data" / "luftdaten.feather")