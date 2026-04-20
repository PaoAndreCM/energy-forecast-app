import requests
import time
from bisect import bisect_left
from config import SEQ_LEN, PRED_LEN, OFFSET,OFFSET_HOURS, SMARD_BASE_URL
import numpy as np
import pandas as pd
import holidays
from datetime import timedelta
import pickle
import torch



# from deutschland import feiertage

# configuration = feiertage.Configuration(
#     host = "https://feiertage-api.de/api"
# )

WEEK_ms = 7 * 24 * 60 * 60 * 1000 # milliseconds in week

def prepare_model_input(df):
    # Load scaler
    with open('models/scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)

    # Select feature columns (everything except 'timestamp' and 'date')
    df_features = df.drop(columns=['timestamp', 'date'])

    # reorder columns so consumption is last column (model expects it last)
    cols = [c for c in df_features.columns if c != 'consumption'] + ['consumption']
    df_features = df_features[cols]

    # Convert to numpy: values
    values = df_features.values

    # Scale
    scaled = scaler.transform(values)

    # Tensorize and unsqueeze
    tensor = torch.FloatTensor(scaled)
    tensor = tensor.unsqueeze(0)

    return tensor

def fetch_available_timestamps():
    """Fetch available timestamps. The available timestamps correspond to the beginning of each week.
    These timestamps can then be used to fetch the consumption corresponding to that week.
    """

    url = SMARD_BASE_URL+'index_quarterhour.json'

    response = requests.get(url)
    response.raise_for_status()
    # TODO handle status error

    data = response.json()
    return data.get('timestamps', [])

def add_time_features (consumption):
    df = pd.DataFrame(consumption, columns=['timestamp', 'consumption'])

    # secs in:
    minute = 60
    hour = 60*minute
    day = 24*hour
    week = 7*day
    year = (365.2425)*day
    month = year/12
    timestamp_s = df['timestamp']/1000

    de_holidays = holidays.Germany(state='HH')

    # Model expects: date,Weekday,Hour sin,Hour cos,Day sin,Day cos,Week sin,Week cos,Month sin,Month cos,Year sin,Year cos,Is Holiday,OT
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['Weekday'] = [n.day_of_week for n in df['date']]
    df['Hour sin'] = np.sin(timestamp_s * (2 * np.pi / hour))
    df['Hour cos'] = np.cos(timestamp_s * (2 * np.pi / hour))
    df['Day sin'] = np.sin(timestamp_s * (2 * np.pi / day))
    df['Day cos'] = np.cos(timestamp_s * (2 * np.pi / day))
    df['Week sin'] = np.sin(timestamp_s * (2 * np.pi / week))
    df['Week cos'] = np.cos(timestamp_s * (2 * np.pi / week))
    df['Month sin'] = np.sin(timestamp_s * (2 * np.pi / month))
    df['Month cos'] = np.cos(timestamp_s * (2 * np.pi / month))
    df['Year sin'] = np.sin(timestamp_s * (2 * np.pi / year))
    df['Year cos'] = np.cos(timestamp_s * (2 * np.pi / year))
    df['Is Holiday'] = [1 if n.date() in de_holidays else (0.5 if n.date() + timedelta(days=1) in de_holidays else 0) for n in df['date']]

    return df

def stitch_consumption(consumption_init, monday_ts, input_start):
    next_monday_ts = monday_ts + WEEK_ms
    consumption = consumption_init + fetch_week_consumption(next_monday_ts)

    for i, pair in enumerate(consumption):
        if pair[0] >= input_start:
            start_index = i
            break
    
    return consumption[start_index:start_index+SEQ_LEN]

def fetch_week_consumption(monday_ts):
    """Fetch consumption corresponding to the week starting on the Monday containing the timestamp
    Args:
        week_start_ts (int) Unix timestamp in ms for a Monday at 00.00
    """

    url = f'{SMARD_BASE_URL}410_DE_quarterhour_{monday_ts}.json'

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    return data.get('series', [])

def calculate_start_of_week(timestamp):
    """Calculate the timestamp for Monday 00.00 of the week containing the given timestamp 
    Args: 
        timestamp (int): Unix timestamp in ms"""
    
    available = fetch_available_timestamps()

    index = bisect_left(available, timestamp)

    if available[index] != timestamp:
        if index != 0:
            index -= 1
        else:
            # TODO handle this error properly
            print("start of week not available as fetchable timestamp")

    monday_ts = available[index]
    return monday_ts

def calculate_input_start_timestamp(timestamp):

    # input starts at timestamp - offset in ms - week in ms
    input_start = timestamp - (OFFSET_HOURS*60*60*1000) - WEEK_ms
    return input_start

def get_input(timestamp):
    """Take desired forecast timestamp and return input needed for model to generate forecast"""

    input_start = calculate_input_start_timestamp(timestamp)
    monday_ts = calculate_start_of_week(input_start)
    consumption = fetch_week_consumption(monday_ts) # each item is a tuple [timestamp, consumption [MWh]]

    if monday_ts != input_start:
        consumption = stitch_consumption(consumption, monday_ts, input_start)
    
    model_input = add_time_features(consumption)

    model_input_tensor = prepare_model_input(model_input)

    return model_input_tensor

# Test
if __name__ == "__main__":
    test_timestamp = 1741682931691
    input = get_input(test_timestamp)
    
    print(input.shape)