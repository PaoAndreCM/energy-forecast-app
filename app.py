# app.py
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'src'))
import streamlit as st
from predict import predict
import time
from datetime import datetime, timedelta
import pandas as pd

# Title
st.title("Germany Electricity Consumption Forecast")
st.write("Select a time and a date and click 'Predict' to obtain the day-ahead forecasted energy consumption.")


# Calculate default date
now = datetime.now()
if now.hour >= 10:
    default_date = (now + timedelta(days=1)).date()  # Tomorrow
else:
    default_date = now.date()  # Today

default_time = datetime.strptime("00:00", "%H:%M").time()  # Midnight

# Use in widgets
date_i = st.date_input(label="Select start of prediction date", value=default_date)
time_i = st.time_input(label="Select start of prediction time", value=default_time)

# Button
if st.button("Predict"):
    # Convert date+time → timestamp
    d = datetime.combine(date_i,time_i)
    timestamp = int(time.mktime(d.timetuple()) * 1000)
    # Call predict(timestamp)
    predictions = predict(timestamp)
    # Display chart
    df = pd.DataFrame({
        'Consumption (MWh)': predictions
    })
    
    st.line_chart(df, height=400)