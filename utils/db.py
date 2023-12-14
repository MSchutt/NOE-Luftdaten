import clickhouse_connect
from clickhouse_connect.driver.client import Client
from clickhouse_connect import common
import streamlit as st

from constants.database import DB_HOST, DB_PASSWORD, DB_PORT, DB_USERNAME

common.set_setting('autogenerate_session_id', False)  # This should always be set before creating a client

@st.cache_resource
def get_db() -> Client:
    return clickhouse_connect.create_client(
        host=DB_HOST,
        port=DB_PORT,
        username=DB_USERNAME,
        password=DB_PASSWORD,
        secure=True
    )