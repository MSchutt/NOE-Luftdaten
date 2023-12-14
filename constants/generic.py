import pandas as pd
import pytz

# Some coordinate in lower austria which is used a map center so that lower austria is centered in the map.
NOE_MAP_CENTER = (48.1937506, 15.5646155)

# Columns we always want to keep
ALWAYS_KEEP_COLUMNS = ["Station", "Longitude", "Latitude", "Altitude", "Datetime"]


# Defaults for the filter
DEFAULT_START_DATE = pd.Timestamp(year=2017, month=1, day=1, tzinfo=pytz.UTC).to_pydatetime()
DEFAULT_END_DATE = pd.Timestamp(year=2022, month=12, day=31, tzinfo=pytz.UTC).to_pydatetime()
DEFAULT_STATION = "St. Pölten"
DEFAULT_SENSOR = "T"

# Maximum Number of Stations to select
MAX_STATIONS_SELECT = 3

# Column names
DATETIME_COLUMN = "Datetime"
MEAN_COLUMN_NAME = "Durchschnitt"

# Table Name
LUFTDATEN_TABLE = "luftdaten_clean"
LUFTDATEN_YEARLY_AGG_TABLE = "luftdaten_yearly_agg"
LUFTDATEN_MONTHLY_AGG_TABLE = "luftdaten_monthly_agg"
LUFTDATEN_WEEKLY_AGG_TABLE = "luftdaten_weekly_agg"
LUFTDATEN_DAILY_AGG_TABLE = "luftdaten_daily_agg"
LUFTDATEN_HOURLY_AGG_TABLE = "luftdaten_hourly_agg"
