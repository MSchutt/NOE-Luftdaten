
import pandas as pd

from constants.generic import LUFTDATEN_DAILY_AGG_TABLE, LUFTDATEN_HOURLY_AGG_TABLE
from utils.db import get_db


def get_aggregated_extreme_values(year: int, use_min = False, table_name = LUFTDATEN_HOURLY_AGG_TABLE) -> pd.DataFrame:
    """
    Retrieves the hourly extreme values for air quality parameters for a given year.

    Args:
        year (int): The year for which to retrieve the extreme values.

    Returns:
        pandas.DataFrame: A DataFrame containing the extreme values for each air quality parameter.
    """
    db = get_db()
    
    rank_order = "ASC" if use_min else "DESC"
    
    qry = f"""
    -- First get the rank of each column
    WITH RankedData AS (
        SELECT
            *,
            ROW_NUMBER() OVER (PARTITION BY NULL ORDER BY G {rank_order}) AS Rank_G,
            ROW_NUMBER() OVER (PARTITION BY NULL ORDER BY NO {rank_order}) AS Rank_NO,
            ROW_NUMBER() OVER (PARTITION BY NULL ORDER BY NO2 {rank_order}) AS Rank_NO2,
            ROW_NUMBER() OVER (PARTITION BY NULL ORDER BY O3 {rank_order}) AS Rank_O3,
            ROW_NUMBER() OVER (PARTITION BY NULL ORDER BY PM10 {rank_order}) AS Rank_PM10,
            ROW_NUMBER() OVER (PARTITION BY NULL ORDER BY PM2_5 {rank_order}) AS Rank_PM2_5,
            ROW_NUMBER() OVER (PARTITION BY NULL ORDER BY T {rank_order}) AS Rank_T
        FROM (SELECT * FROM {table_name} where year(Datetime) = %(year)s)
    )
    -- then select from that and find out which column is the max
    SELECT
        Station,
        Datetime,
        G,
        NO,
        NO2,
        O3,
        PM10,
        PM2_5,
        T,
        -- alternative to CASE WHEN (kind of ClickHouse specific)
        multiIf(Rank_G = 1, 'G', Rank_NO = 1, 'NO', Rank_NO2 = 1, 'NO2', Rank_O3 = 1, 'O3', Rank_PM10 = 1, 'PM10', Rank_PM2_5 = 1, 'PM2_5', Rank_T = 1, 'T', 'Not available') AS max_col
    FROM RankedData
    WHERE
        Rank_G = 1 OR
        Rank_NO = 1 OR
        Rank_NO2 = 1 OR
        Rank_O3 = 1 OR
        Rank_PM10 = 1 OR
        Rank_PM2_5 = 1 OR
        Rank_T = 1
    ORDER BY max_col    
    """
    
    return db.query_df(qry, { "year": year })