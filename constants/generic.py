import pandas as pd

# Some coordinate in lower austria which is used a map center so that lower austria is centered in the map.
NOE_MAP_CENTER = (48.1937506, 15.5646155)

# Columns we always want to keep
ALWAYS_KEEP_COLUMNS = ["Station", "Datetime_Start", "Datetime_End", "Longitude", "Latitude", "Altitude"]


# Defaults for the filter
DEFAULT_START_DATE = pd.Timestamp(year=2017, month=1, day=1).to_pydatetime()
DEFAULT_END_DATE = pd.Timestamp(year=2022, month=12, day=31).to_pydatetime()
DEFAULT_STATION = "St. Pölten"
DEFAULT_SENSOR = "T"

# Column names
DATETIME_COLUMN = "Datetime_Start"
MEAN_COLUMN_NAME = "Durchschnitt"