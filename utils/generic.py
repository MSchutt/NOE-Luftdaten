import streamlit as st
import pandas as pd
from pathlib import Path
from typing import List, Tuple
from constants.generic import LUFTDATEN_TABLE
from datetime import datetime

from utils.db import get_db


def db_get_stations() -> List[str]:
    db = get_db()
    
    stations = db.query_df(f"SELECT DISTINCT Station FROM {LUFTDATEN_TABLE} ORDER BY Station ASC")
    if len(stations) == 0:
        return []
    
    return stations["Station"].tolist()


def db_get_daterange() -> Tuple[datetime, datetime]:
    db = get_db()
    
    dates = db.query_df(f"SELECT MIN(Datetime_Start) AS min, MAX(Datetime_Start) AS max FROM {LUFTDATEN_TABLE}")
    
    if len(dates) == 0:
        return []
    
    return (dates["min"].iloc[0].to_pydatetime(), dates["max"].iloc[0].to_pydatetime())