import clickhouse_connect
from clickhouse_connect.driver.client import Client
from clickhouse_connect import common
import streamlit as st

common.set_setting('autogenerate_session_id', False)  # This should always be set before creating a client

@st.cache_resource
def get_db() -> Client:
    return clickhouse_connect.create_client(
        host=st.secrets["DB_HOST"],
        port=st.secrets["DB_PORT"],
        username=st.secrets["DB_USERNAME"],
        password=st.secrets["DB_PASSWORD"],
        secure=True
    )