# app.py
import sys
from pathlib import Path
import altair as alt
from random import randint

sys.path.insert(0, str(Path(__file__).parent / 'src'))
import streamlit as st
from predict import predict
import time
from datetime import datetime, timedelta
import pandas as pd

st.title("Day-Ahead Germany Electricity Consumption Forecast")

st.write("Select a date and time to get a 24-hour electricity consumption forecast for Germany.")

st.markdown("""
**How it works:**
1. Choose your forecast start time below
2. The model uses 7 days of historical data from SMARD API
3. Predicts the next 24 hours of grid consumption (96 datapoints at 15-min intervals)

**Model:** PatchTST transformer trained on 2015-2020 German grid data

*Note: Forecasts are limited by real-time data availability (typically up to ~14 hours ahead)*
""")


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

    # Create time labels (96 15-min intervals)
    times = [d + timedelta(minutes=15*i) for i in range(96)]
    print("\n" + str(times))
    
    # Create DataFrame with formatted time strings
    df = pd.DataFrame({
        'Time': [t.strftime('%Y/%m/%d %H:%M') for t in times],  # Format as HH:MM
        'Consumption (MWh)': predictions
    })

    chart = alt.Chart(df).mark_line().encode(
    alt.X("Time", scale=alt.Scale(type="utc"), sort=None),
    alt.Y("Consumption (MWh)")
    )
    st.altair_chart(chart)