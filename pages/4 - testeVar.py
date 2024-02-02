import streamlit as st
import os

db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
db_host = os.environ.get('DB_HOST')
db_port = os.environ.get('DB_PORT')
db_database = os.environ.get('DB_DATABASE')

st.info(db_user)
st.info(db_password)
st.info(db_host)
st.info(db_port)
st.info(db_database)
